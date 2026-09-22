from datetime import date


def get_trip_months(
    start_date: date,
    end_date: date
) -> list[int]:

    if end_date < start_date:
        raise ValueError(
            'end_date must be greater than or equal to start_date'
        )

    months = []

    current_year = start_date.year
    current_month = start_date.month

    while True:

        months.append(current_month)

        if (
            current_year == end_date.year
            and current_month == end_date.month
        ):
            break

        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    return months