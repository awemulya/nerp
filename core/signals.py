from django.dispatch import Signal

fiscal_year_signal = Signal(providing_args=["new_fiscal_year_str", "new_fiscal_year", "old_fiscal_year"])


