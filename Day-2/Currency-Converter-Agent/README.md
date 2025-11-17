# Currency Converter Agent
### Description:
this agent will convert currency from one denomination to another and calculates the fees to do the conversation. The Agent has two custom tools and follow the workflows:
```
1. Free Lookup Tools - Finds transaction fees for the conversion (mock)
2. Exchange Rate Tools - Gets currency conversation rates (mock)
3. Calculation Setup - Calculates the total conversation cost includign fees.
```
workflow:
```
1. user -> 2. Currency-Agent -> 3. {(get-fee-for-payment-method) | (get-exchange-rate)}
```
