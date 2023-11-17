# Get recommendations for a specific users

In this use-case, we emulate an e-commerce backend that wants to build a recommendation system for their products.
The flow is as follows:
- The user visits a specific products
- The backend returns a list of recommended products that are part of the product catalog, with metadata about the product


## Setup
First we set up the Astra database:

```bash
export ASTRA_DB_ENDPOINT=https://xxx.astra.datasta.com
export ASTRA_DB_TOKEN=AstraCS:xxx
```

Then we index the products and we create two registered users:

```bash
python3 recommendations/setup_all.py
```

Then we simulate the user to product interactions:

```bash
python3 recommendations/get_recommendation.py

  User handle? ['max', 'adele']
  max
  Product?
  TV 4K
```

Now we expect few products that are a good match to buy with the 'TV 4K'.
The user handle is used to identify the user, the recommendation system will look up the user profile to get more information about the user.

```
Digital Photo Frame - 50$. A digital photo frame would be a great addition to your TV, allowing you to display your favorite photos in high resolution. It is a more affordable option compared to buying another TV.
Smart Home Security Camera - 120$. A smart home security camera would complement your TV by providing added security to your home. It offers motion detection and two-way audio, allowing you to monitor your home remotely.
Smart Doorbell - 130$. A smart doorbell would be a great addition to your TV, providing you with video surveillance and two-way communication at your front door. It offers similar features to a security camera but with the added benefit of being a doorbell.
```