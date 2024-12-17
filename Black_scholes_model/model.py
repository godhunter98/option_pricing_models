# Import required libraries
import math  # For mathematical functions like logarithm and exponential
from scipy.stats import (
    norm,
)  # For cumulative distribution function (CDF) of the normal distribution


class OptionPricingModel:
    """
    This class implements the Black-Scholes-Merton (BSM) formula
    to calculate d1, d2, and other related components for European option pricing.
    """

    def __init__(self, spot, strike_price, rfr, volatility, time_to_expiry) -> None:
        """
        Initializes the OptionPricingModel with required inputs.

        :param spot: Current price of the underlying asset
        :param strike_price: Strike price of the option
        :param rfr: Risk-free rate (annualized, as a decimal)
        :param volatility: Volatility of the underlying asset (annualized, as a decimal)
        :param time_to_expiry: Time to expiry of the option in years
        """
        self.spot = spot
        self.strike_price = strike_price
        self.rfr = rfr
        self.volatility = volatility
        self.time_to_expiry = time_to_expiry

    def d1(self):
        """
        Calculates d1, a key component in the BSM formula.

        Formula:
        d1 = [ln(S / X) + (r + (v^2 / 2)) * T] / [v * sqrt(T)]

        :return: Rounded value of d1
        """
        s, x, v, t, r = (
            self.spot,
            self.strike_price,
            self.volatility,
            self.time_to_expiry,
            self.rfr,
        )
        formula = ((math.log(s / x)) + ((r + (v**2) / 2) * t)) / (v * math.sqrt(t))
        return round(formula, 3)

    def d2(self):
        """
        Calculates d2, a component derived from d1.

        Formula:
        d2 = d1 - v * sqrt(T)

        :return: Rounded value of d2
        """
        return round(self.d1() - (self.volatility * math.sqrt(self.time_to_expiry)), 3)

    def normsd1(self):
        """
        Calculates N(d1), the cumulative probability of d1 under the standard normal distribution.

        :return: Rounded value of N(d1)
        """
        return round(norm.cdf(self.d1()), 3)

    def normsd2(self):
        """
        Calculates N(d2), the cumulative probability of d2 under the standard normal distribution.

        :return: Rounded value of N(d2)
        """
        return round(norm.cdf(self.d2()), 3)

    def call_option_price(self):
        """
        Calculates the price of a European Call Option using the BSM formula.

        Formula for Call Option:
        Call Price = S * N(d1) - X * exp(-r * T) * N(d2)

        :return: Call option price
        """
        return (self.spot * self.normsd1()) - (
            self.strike_price
            * math.exp(-self.rfr * self.time_to_expiry)
            * self.normsd2()
        )

    def put_option_price(self):
        """
        Calculates the price of a European Put Option using the BSM formula.

        Formula for Put Option:
        Put Price = X * exp(-r * T) * N(-d2) - S * N(-d1)

        :return: Put option price
        """
        # Explicitly calculate N(-d1) and N(-d2)
        nd1_neg = round(norm.cdf(-self.d1()), 3)
        nd2_neg = round(norm.cdf(-self.d2()), 3)

        return (
            self.strike_price * math.exp(-self.rfr * self.time_to_expiry) * nd2_neg
        ) - (self.spot * nd1_neg)


def main():
    """
    Main function to take user inputs and calculate d1, d2, N(d1), N(d2),
    and both Call and Put option prices using the OptionPricingModel class.
    """
    # Gather inputs from the user
    spot = float(input("Where is the spot trading currently? "))
    strike_price = float(input("What is the strike price for the option? "))
    rfr = float(input("What is the current risk-free rate (RFR, in %)? ")) / 100
    volatility = float(input("What is the current volatility (VIX, in %)? ")) / 100
    time_to_expiry = float(input("What is the time to expiry (in years)? "))

    # Initialize the option pricing model
    option_model = OptionPricingModel(
        spot, strike_price, rfr, volatility, time_to_expiry
    )

    # Display calculated values
    print(f"d1: {option_model.d1()}")
    print(f"d2: {option_model.d2()}")
    print(f"N(d1): {option_model.normsd1()}")
    print(f"N(d2): {option_model.normsd2()}")
    print(f"Call Option Price: {option_model.call_option_price()}")
    print(f"Put Option Price: {option_model.put_option_price()}")


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
