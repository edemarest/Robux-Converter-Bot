## Overview
This bot provides currency conversion between Robux (R$) and various real-world currencies using Discord slash commands.

## Features
- Convert Robux to real-world currency (`/robux2money`)
- Convert real-world currency to Robux (`/money2robux`)
- Supports multiple currencies including USD, EUR, JPY, GBP, and more

## Commands

### `/robux2money`
**Description:** Convert Robux (R$) to real-world currency.

**Usage:**
```
/robux2money robux: <amount> currency: <currency_code>
```
- `robux`: The amount of Robux to convert.
- `currency` (default: USD): The target currency code.

**Example:**
```
/robux2money robux: 1000 currency: EUR
```
**Response:**
```
💰 1,000 R$ is approximately €2.98 in DevEx rates.
```

### `/money2robux`
**Description:** Convert real-world currency to Robux (R$).

**Usage:**
```
/money2robux amount: <amount> currency: <currency_code>
```
- `amount`: The amount of money to convert.
- `currency` (default: USD): The input currency code.

**Example:**
```
/money2robux amount: 10 currency: USD
```
**Response:**
```
💰 $10.00 is approximately 2,857 R$ in DevEx rates.
```

## Supported Currencies
- `USD`, `EUR`, `JPY`, `GBP`, `AUD`, `CAD`, `CHF`, `CNY`, `HKD`, `NZD`, `SEK`, `KRW`, `SGD`, `NOK`, `MXN`

## How It Works
1. Listens for `/robux2money` and `/money2robux` commands.
2. Defaults to `USD` if an unsupported currency is provided.
3. Converts Robux to USD at **1000 R$ = $3.50**.
4. Converts USD to the target currency using predefined rates.
5. Displays the converted value in a formatted message.
