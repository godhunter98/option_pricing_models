# Import required libraries
import math  # For mathematical functions like logarithm and exponential
from scipy.stats import norm  # For cumulative distribution function (CDF) of the normal distribution


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
        :param rfr: Risk-free rate (annualized)
        :param volatility: Volatility of the underlying asset (annualized)
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
        formula = ((math.log(s / x)) + ((v**2) / 2) * t + (r * t)) / (v * (t**0.5))
        return round(formula, 3)

    def d2(self):
        """
        Calculates d2, a component derived from d1.

        Formula:
        d2 = d1 - v * sqrt(T)

        :return: Rounded value of d2
        """
        return round(self.d1() - (self.volatility * (self.time_to_expiry**0.5)), 3)

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

    def option_price(self):
        """
        Calculates the price of the European option using the BSM formula.

        Formula for Call Option:
        Option Price = S * N(d1) - X * exp(-r * T) * N(d2)

        :return: Option price
        """
        return (self.spot * self.normsd1()) - (
            math.exp(-self.rfr * self.time_to_expiry) * self.normsd2()
        )


def main():
    """
    Main function to take user inputs and calculate d1, d2, N(d1), and N(d2)
    using the OptionPricingModel class.
    """
    # Gather inputs from the user
    spot = int(input("Where is the spot trading currently? "))
    strike_price = int(
        input("Whats the strike price for whom you want to price the option? ")
    )

    # Convert rates to decimals (e.g., 5% input -> 0.05)
    rfr = (
        int(input("What is the current RFR? ")) / 100
    )  # Risk-free rate input
    Volatility = (
        int(input("What is the current Volatility(VIX)? ")) / 100
    )  # Volatility input
    Time_to_expiry = float(input("What is the time do expiry from today (In years)? "))

    # Initialize the option pricing model
    option_model = OptionPricingModel(
        spot, strike_price, rfr, Volatility, Time_to_expiry
    )

    # Display calculated values
    print(f"d1: {option_model.d1()}")
    print(f"d2: {option_model.d2()}")
    print(f"N(d1): {option_model.normsd1()}")
    print(f"N(d2): {option_model.normsd2()}")


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
