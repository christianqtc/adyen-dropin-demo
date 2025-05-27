async function startCheckout() {
  try {
    const response = await fetch("/api/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const session = await response.json();

    const configuration = {
      environment: "test",
      clientKey: clientKey,
      session,
      locale: "en_US",
      countryCode: "US",
      showPayButton: true,
      onPaymentCompleted: () => alert("Payment successful."),
      onPaymentFailed: () => alert("Payment failed. Please try again."),
      onError: () => alert("An error occurred. Please try again.")
    };

    const paymentMethodsConfiguration = {
      card: {
        showBrandIcon: true,
        hasHolderName: true,
        holderNameRequired: true,
        amount: { value: 1000, currency: "USD" },
        placeholders: {
          cardNumber: "4111 1111 1111 1111",
          expiryDate: "03/30",
          securityCode: "737",
          holderName: "John Smith"
        }
      }
    };

    const checkout = await AdyenCheckout({
      ...configuration,
      paymentMethodsConfiguration
    });

    checkout.create("dropin").mount("#dropin-container");
  } catch {
    alert("Failed to initialize Drop-in.");
  }
}

window.addEventListener("DOMContentLoaded", startCheckout);
