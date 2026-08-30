import yfinance as yf
import matplotlib.pyplot as plt


def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date
    )

    if data.empty:
        return None

    return data


def calculate_metrics(data):
    close = data["Close"].squeeze()
    volume = data["Volume"].squeeze()

    data["SMA_20"] = close.rolling(window=20).mean()
    data["SMA_50"] = close.rolling(window=50).mean()
    data["SMA_200"] = close.rolling(window=200).mean()

    data["Daily_Return"] = close.pct_change()

    starting_price = close.iloc[0]
    latest_price = close.iloc[-1]
    highest_price = close.max()
    lowest_price = close.min()

    total_return = (
        (latest_price - starting_price)
        / starting_price
    ) * 100

    average_daily_volume = volume.mean()
    average_daily_return = data["Daily_Return"].mean()
    daily_volatility = data["Daily_Return"].std()

    running_max = close.cummax()
    drawdown = (close - running_max) / running_max
    max_drawdown = drawdown.min() * 100

    if latest_price > data["SMA_20"].iloc[-1]:
        short_term_trend = "Bullish"
    else:
        short_term_trend = "Bearish"

    metrics = {
        "starting_price": starting_price,
        "latest_price": latest_price,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
        "total_return": total_return,
        "average_daily_volume": average_daily_volume,
        "average_daily_return": average_daily_return,
        "daily_volatility": daily_volatility,
        "max_drawdown": max_drawdown,
        "short_term_trend": short_term_trend
    }

    return metrics


def display_summary(ticker, metrics):
    print("\n")
    print("================================")
    print("          STOCK SUMMARY")
    print("================================")

    print(f"Ticker: {ticker}")
    print(f"Starting Price: ${metrics['starting_price']:.2f}")
    print(f"Latest Price: ${metrics['latest_price']:.2f}")
    print(f"Highest Price: ${metrics['highest_price']:.2f}")
    print(f"Lowest Price: ${metrics['lowest_price']:.2f}")
    print(f"Total Return: {metrics['total_return']:.2f}%")
    print(
        f"Average Daily Volume: "
        f"{metrics['average_daily_volume']:,.0f}"
    )
    print(
        f"Average Daily Return: "
        f"{metrics['average_daily_return'] * 100:.4f}%"
    )
    print(
        f"Daily Volatility: "
        f"{metrics['daily_volatility'] * 100:.2f}%"
    )
    print(
        f"Maximum Drawdown: "
        f"{metrics['max_drawdown']:.2f}%"
    )
    print(f"Short-Term Trend: {metrics['short_term_trend']}")


def plot_stock_data(data, ticker):
    close = data["Close"].squeeze()
    volume = data["Volume"].squeeze()

    plt.figure(figsize=(12, 10))

    plt.subplot(3, 1, 1)

    plt.plot(close, label="Closing Price")
    plt.plot(data["SMA_20"], label="20-Day SMA")
    plt.plot(data["SMA_50"], label="50-Day SMA")
    plt.plot(data["SMA_200"], label="200-Day SMA")

    plt.title(f"{ticker} Stock Analysis")
    plt.ylabel("Price")

    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)

    plt.bar(volume.index, volume)

    plt.xlabel("Date")
    plt.ylabel("Volume")

    plt.grid(True)

    plt.subplot(3, 1, 3)

    plt.plot(
        data["Daily_Return"] * 100,
        label="Daily Return"
    )

    plt.axhline(
        0,
        linestyle="--"
    )

    plt.xlabel("Date")
    plt.ylabel("Return (%)")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.show()


def main():
    ticker = input("Enter stock ticker: ").upper()

    start_date = input(
        "Enter start date (YYYY-MM-DD): "
    )

    end_date = input(
        "Enter end date (YYYY-MM-DD): "
    )

    data = fetch_stock_data(
        ticker,
        start_date,
        end_date
    )

    if data is None:
        print("\nNo data found.")
        print("Please check the stock ticker and date range.")
        return

    metrics = calculate_metrics(data)

    display_summary(
        ticker,
        metrics
    )

    plot_stock_data(
        data,
        ticker
    )


if __name__ == "__main__":
    main()