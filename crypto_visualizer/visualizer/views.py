from datetime import UTC
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from pycoingecko import CoinGeckoAPI


def index(request):
    cg = CoinGeckoAPI()
    currency = "usd"
    currency_id = "bitcoin"

    if request.method == "POST":
        currency = request.POST.get("selected_currency")
        currency_id = request.POST.get("selected_option")

        data = cg.get_coin_market_chart_by_id(
            id=currency_id,
            vs_currency=currency,
            days=100,
            interval="daily",
        )
        first_elements = [lst[0] for lst in data["prices"]]
        actual_price = [lst[1] for lst in data["prices"]]

        timestamps_seconds = [ts / 1000 for ts in first_elements]
        date_times = [datetime.fromtimestamp(ts, tz=UTC) for ts in timestamps_seconds]
        date_time_strings = [dt.strftime("%A %d %B") for dt in date_times]

        return JsonResponse(
            {
                "crypData": date_time_strings[0:100],
                "actualPrice": actual_price[0:100],
                "currency": currency,
            },
        )

    data = cg.get_coin_market_chart_by_id(
        id=currency_id,
        vs_currency=currency,
        days=100,
        interval="daily",
    )
    first_elements = [lst[0] for lst in data["prices"]]
    actual_price = [lst[1] for lst in data["prices"]]
    timestamps_seconds = [ts / 1000 for ts in first_elements]
    date_times = [datetime.fromtimestamp(ts, tz=UTC) for ts in timestamps_seconds]
    date_time_strings = [dt.strftime("%A %d %B") for dt in date_times]

    market_data = cg.get_coins_markets(
        vs_currency="usd",
        order="market_cap_desc",
        per_page=100,
        page=1,
    )
    bar_view_data = list(market_data)

    coin_list = cg.get_coins_list()
    coin_id_list = [item["id"] for item in coin_list]
    currency_symbols = [
        "usd",
        "eur",
        "jpy",
        "gbp",
        "aud",
        "cad",
        "chf",
        "cny",
        "sek",
        "nzd",
        "mxn",
        "sgd",
        "hkd",
        "nok",
        "krw",
        "inr",
        "rub",
        "brl",
        "zar",
        "try",
    ]
    exchange_rates = cg.get_exchange_rates()
    portfolio_data = market_data[0:10]

    return render(
        request,
        "visualizer/base.html",
        {
            "content1": {
                "template_name": "visualizer/chart.html",
                "data": {
                    "crypData": date_time_strings[0:100],
                    "actualPrice": actual_price[0:100],
                    "currency": currency,
                    "coin_id_list": coin_id_list,
                    "currency_symbols": currency_symbols,
                },
            },
            "content2": {
                "template_name": "visualizer/exchange.html",
                "data": {"exchange_rates": exchange_rates},
            },
            "content3": {
                "template_name": "visualizer/barView.html",
                "data": {"bar_view_data": bar_view_data},
            },
            "content4": {
                "template_name": "visualizer/pieChart.html",
                "data": {"portfolio_data": portfolio_data},
            },
        },
    )
