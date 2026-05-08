#!/usr/bin/env python3
import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import median


@dataclass
class Trade:
    entry_date: str
    exit_date: str
    return_pct: float
    reason: str


def available_assets(root: Path) -> list[str]:
    market_data = root / "Agents" / "Tools" / "Market_data"
    assets = []
    for path in market_data.iterdir():
        if path.is_dir() and (path / "historical_data.json").exists():
            assets.append(path.name)
    return sorted(assets)


def choose_asset(root: Path) -> str:
    assets = available_assets(root)
    if not assets:
        raise SystemExit("No hay activos disponibles en Agents/Tools/Market_data.")

    print("Activos disponibles:")
    for index, asset in enumerate(assets, start=1):
        print(f"  {index}. {asset}")

    while True:
        value = input("Selecciona ticker por numero o nombre: ").strip()
        if value.isdigit():
            index = int(value)
            if 1 <= index <= len(assets):
                return assets[index - 1]
        upper = value.upper()
        if upper in assets:
            return upper
        print("Seleccion no valida.")


def load_daily_candles(root: Path, asset: str) -> tuple[list[str], dict[str, list[dict]]]:
    path = root / "Agents" / "Tools" / "Market_data" / asset / "historical_data.json"
    with path.open() as f:
        candles = json.load(f)

    by_date: dict[str, list[dict]] = {}
    for candle in candles:
        date = candle["datetime"][:10]
        by_date.setdefault(date, []).append(candle)

    for day in by_date.values():
        day.sort(key=lambda item: item["datetime"])

    return sorted(by_date), by_date


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def first_candle(day: list[dict]) -> dict:
    return next((c for c in day if c["datetime"].endswith("09:30:00")), day[0])


def run_backtest(
    dates: list[str],
    by_date: dict[str, list[dict]],
    start: str,
    gap_pct: float,
    hold_sessions: int,
    stop_pct: float | None,
    no_overlap: bool,
) -> list[Trade]:
    trades: list[Trade] = []
    i = 1

    while i < len(dates):
        if dates[i] < start:
            i += 1
            continue
        if i + hold_sessions >= len(dates):
            break

        prev_day = by_date[dates[i - 1]]
        day = by_date[dates[i]]
        opening = first_candle(day)
        previous_close = prev_day[-1]["close"]
        gap = (opening["open"] - previous_close) / previous_close * 100

        if gap <= gap_pct:
            i += 1
            continue

        entry = opening["open"]
        exit_price = None
        exit_index = None
        reason = "fixed"

        if stop_pct is not None:
            stop_price = entry * (1 - stop_pct / 100)
            for j in range(i, i + hold_sessions + 1):
                for candle in by_date[dates[j]]:
                    if candle["low"] <= stop_price:
                        exit_price = stop_price
                        exit_index = j
                        reason = "stop"
                        break
                if exit_price is not None:
                    break

        if exit_price is None:
            exit_index = i + hold_sessions
            exit_price = by_date[dates[exit_index]][-1]["close"]

        trades.append(
            Trade(
                entry_date=dates[i],
                exit_date=dates[exit_index],
                return_pct=(exit_price - entry) / entry * 100,
                reason=reason,
            )
        )

        i = exit_index + 1 if no_overlap else i + 1

    return trades


def summarize(trades: list[Trade], initial_capital: float) -> dict:
    capital = initial_capital
    peak = initial_capital
    max_drawdown = 0.0

    returns = [trade.return_pct for trade in trades]
    for ret in returns:
        capital *= 1 + ret / 100
        peak = max(peak, capital)
        max_drawdown = min(max_drawdown, (capital - peak) / peak * 100)

    wins = [ret for ret in returns if ret > 0]
    losses = [ret for ret in returns if ret < 0]

    return {
        "trades": len(trades),
        "capital_final": capital,
        "rentabilidad_pct": (capital / initial_capital - 1) * 100,
        "sube_pct": len(wins) / len(trades) * 100 if trades else 0,
        "media": mean(returns),
        "mediana": median(returns) if returns else 0,
        "media_subida": mean(wins),
        "media_bajada": mean(losses),
        "max_subida": max(returns) if returns else 0,
        "max_bajada": min(returns) if returns else 0,
        "max_drawdown": max_drawdown,
        "stops": sum(1 for trade in trades if trade.reason == "stop"),
    }


def print_markdown(rows: list[dict]) -> None:
    headers = [
        "Sesiones",
        "Casos",
        "Capital final",
        "Rentabilidad",
        "Sube",
        "Media",
        "Mediana",
        "Media subida",
        "Media bajada",
        "Max subida",
        "Max bajada",
        "Max DD",
        "Stops",
    ]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---:" for _ in headers]) + "|")
    for row in rows:
        print(
            "| "
            + " | ".join(
                [
                    f"{row['sessions']}",
                    f"{row['trades']}",
                    f"{row['capital_final']:.2f}",
                    f"{row['rentabilidad_pct']:+.1f}%",
                    f"{row['sube_pct']:.1f}%",
                    f"{row['media']:+.2f}%",
                    f"{row['mediana']:+.2f}%",
                    f"{row['media_subida']:+.2f}%",
                    f"{row['media_bajada']:+.2f}%",
                    f"{row['max_subida']:+.2f}%",
                    f"{row['max_bajada']:+.2f}%",
                    f"{row['max_drawdown']:+.1f}%",
                    f"{row['stops']}",
                ]
            )
            + " |"
        )


def parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def print_grid(rows: list[dict], limit: int) -> None:
    headers = [
        "Rank",
        "Gap",
        "Stop",
        "Sesiones",
        "Casos",
        "Capital final",
        "Rentabilidad",
        "Sube",
        "Mediana",
        "Max DD",
        "Stops",
    ]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---:" for _ in headers]) + "|")
    for rank, row in enumerate(rows[:limit], start=1):
        print(
            "| "
            + " | ".join(
                [
                    str(rank),
                    f"{row['gap']:.2f}%",
                    "sin stop" if row["stop"] is None else f"{row['stop']:.2f}%",
                    str(row["sessions"]),
                    str(row["trades"]),
                    f"{row['capital_final']:.2f}",
                    f"{row['rentabilidad_pct']:+.1f}%",
                    f"{row['sube_pct']:.1f}%",
                    f"{row['mediana']:+.2f}%",
                    f"{row['max_drawdown']:+.1f}%",
                    str(row["stops"]),
                ]
            )
            + " |"
        )


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, title: str, rows: list[dict], grid: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    if grid and rows:
        best = rows[0]
        stop = "sin stop" if best["stop"] is None else f"{best['stop']:.2f}%"
        lines.extend(
            [
                "## Mejor estrategia",
                "",
                f"- Gap minimo: **>{best['gap']:.2f}%**",
                f"- Stop: **{stop}**",
                f"- Sesiones: **{best['sessions']}**",
                f"- Capital final: **{best['capital_final']:.2f}**",
                f"- Rentabilidad: **{best['rentabilidad_pct']:+.1f}%**",
                f"- Max drawdown: **{best['max_drawdown']:+.1f}%**",
                "",
            ]
        )

    headers = (
        ["Gap", "Stop", "Sesiones", "Casos", "Capital final", "Rentabilidad", "Sube", "Mediana", "Max DD", "Stops"]
        if grid
        else ["Sesiones", "Casos", "Capital final", "Rentabilidad", "Sube", "Media", "Mediana", "Max DD", "Stops"]
    )
    lines.extend(["| " + " | ".join(headers) + " |", "|" + "|".join(["---:" for _ in headers]) + "|"])
    for row in rows:
        if grid:
            values = [
                f"{row['gap']:.2f}%",
                "sin stop" if row["stop"] is None else f"{row['stop']:.2f}%",
                str(row["sessions"]),
                str(row["trades"]),
                f"{row['capital_final']:.2f}",
                f"{row['rentabilidad_pct']:+.1f}%",
                f"{row['sube_pct']:.1f}%",
                f"{row['mediana']:+.2f}%",
                f"{row['max_drawdown']:+.1f}%",
                str(row["stops"]),
            ]
        else:
            values = [
                str(row["sessions"]),
                str(row["trades"]),
                f"{row['capital_final']:.2f}",
                f"{row['rentabilidad_pct']:+.1f}%",
                f"{row['sube_pct']:.1f}%",
                f"{row['media']:+.2f}%",
                f"{row['mediana']:+.2f}%",
                f"{row['max_drawdown']:+.1f}%",
                str(row["stops"]),
            ]
        lines.append("| " + " | ".join(values) + " |")
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest gap-up strategy on local 4h market data.")
    parser.add_argument("asset", nargs="?", help="Asset folder name, e.g. AAPL or TSLA")
    parser.add_argument("--list-assets", action="store_true", help="List available assets and exit")
    parser.add_argument("--start", default="2023-05-08")
    parser.add_argument("--gap", type=float, default=0.5, help="Minimum opening gap percentage")
    parser.add_argument("--stop", type=float, default=3.0, help="Stop loss percentage. Use 0 to disable.")
    parser.add_argument("--min-hold", type=int, default=1)
    parser.add_argument("--max-hold", type=int, default=7)
    parser.add_argument("--capital", type=float, default=100.0)
    parser.add_argument("--allow-overlap", action="store_true", help="Allow overlapping trades")
    parser.add_argument("--grid-search", action="store_true", help="Try combinations of gap, stop, and hold")
    parser.add_argument("--gaps", default="0,0.25,0.5,0.75,1,1.25,1.5,2")
    parser.add_argument("--stops", default="0,2,2.5,3,4,5,6")
    parser.add_argument("--sort-by", choices=["return", "drawdown", "return_drawdown"], default="return")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--min-trades", type=int, default=20)
    parser.add_argument("--output", help="Optional output file. Supports .csv or .md")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[3]
    if args.list_assets:
        for asset in available_assets(root):
            print(asset)
        return

    asset = args.asset.upper() if args.asset else choose_asset(root)
    dates, by_date = load_daily_candles(root, asset)
    stop = args.stop if args.stop > 0 else None

    if args.grid_search:
        rows = []
        for gap in parse_float_list(args.gaps):
            for stop_value in parse_float_list(args.stops):
                grid_stop = stop_value if stop_value > 0 else None
                for sessions in range(args.min_hold, args.max_hold + 1):
                    trades = run_backtest(
                        dates=dates,
                        by_date=by_date,
                        start=args.start,
                        gap_pct=gap,
                        hold_sessions=sessions,
                        stop_pct=grid_stop,
                        no_overlap=not args.allow_overlap,
                    )
                    if len(trades) < args.min_trades:
                        continue
                    summary = summarize(trades, args.capital)
                    rows.append(
                        {
                            "gap": gap,
                            "stop": grid_stop,
                            "sessions": sessions,
                            **summary,
                        }
                    )

        if args.sort_by == "return":
            rows.sort(key=lambda row: row["rentabilidad_pct"], reverse=True)
        elif args.sort_by == "drawdown":
            rows.sort(key=lambda row: row["max_drawdown"], reverse=True)
        else:
            rows.sort(
                key=lambda row: row["rentabilidad_pct"] / abs(row["max_drawdown"])
                if row["max_drawdown"] < 0
                else float("inf"),
                reverse=True,
            )

        print(
            f"Grid search: {asset} | Solape: {'si' if args.allow_overlap else 'no'} | "
            f"Orden: {args.sort_by}"
        )
        if rows:
            best = rows[0]
            stop = "sin stop" if best["stop"] is None else f"{best['stop']:.2f}%"
            print(
                "MEJOR ESTRATEGIA: "
                f"gap > {best['gap']:.2f}% | stop: {stop} | "
                f"sesiones: {best['sessions']} | "
                f"rentabilidad: {best['rentabilidad_pct']:+.1f}% | "
                f"capital final: {best['capital_final']:.2f} | "
                f"max DD: {best['max_drawdown']:+.1f}%"
            )
        print_grid(rows, args.limit)
        if args.output:
            output = Path(args.output)
            selected = rows[: args.limit]
            if output.suffix.lower() == ".csv":
                write_csv(output, selected)
            elif output.suffix.lower() in {".md", ".markdown"}:
                write_markdown(output, f"Grid search {asset}", selected, grid=True)
            else:
                raise SystemExit("--output debe terminar en .csv o .md")
            print(f"\nGuardado: {output}")
        return

    rows = []
    for sessions in range(args.min_hold, args.max_hold + 1):
        trades = run_backtest(
            dates=dates,
            by_date=by_date,
            start=args.start,
            gap_pct=args.gap,
            hold_sessions=sessions,
            stop_pct=stop,
            no_overlap=not args.allow_overlap,
        )
        summary = summarize(trades, args.capital)
        rows.append({"sessions": sessions, **summary})

    print(
        f"Activo: {asset} | Gap > {args.gap}% | "
        f"Stop: {'sin stop' if stop is None else f'{stop}%'} | "
        f"Solape: {'si' if args.allow_overlap else 'no'}"
    )
    print_markdown(rows)
    if args.output:
        output = Path(args.output)
        if output.suffix.lower() == ".csv":
            write_csv(output, rows)
        elif output.suffix.lower() in {".md", ".markdown"}:
            write_markdown(output, f"Backtest {asset}", rows, grid=False)
        else:
            raise SystemExit("--output debe terminar en .csv o .md")
        print(f"\nGuardado: {output}")


if __name__ == "__main__":
    main()
