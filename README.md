## Problem 1: Revenue Analysis
Attached you will find a CSV file that contains the complete log of orders by customers for a
company. For this particular company we are interested in understanding how much revenue
comes from new customers versus recurring customers. Specifically we want to answer the
following questions:
1. What is the total revenue from orders for each month
2. and, what percent of revenue comes from new customers for each month

A new customer is defined as one that has no previous orders prior to the month we are
examining. That means if customer ‘A’ has two orders on 2020-1-10 and 2020-1-12 and no
orders prior we count the two orders as new customer revenue for the month of January 2020.

Hint: Since the log represents the entire history of orders for the company, we can expect 100%
of the revenue for the first month to come from new customers.

Extra Credit (Optional): Determine the TOTAL revenue gained from customers acquired in each
month. This means for the set of new customers in a particular month, what is the sum of
revenue generated for the current month and all subsequent months.
You may use any tool or language to solve this problem such as Pandas, SQL, R, ect. Be sure
to include both the answers you calculated and any code you’ve written.

```
- Answers for the 1 and 2 questions:
                              amount  new_customer_total  new_customer_percentage
created_at                                                                       
2019-11-30 00:00:00+00:00  130641.56            93851.00                    71.84
2019-12-31 00:00:00+00:00  301773.94           210120.04                    69.63
2020-01-31 00:00:00+00:00  196019.33           140172.50                    71.51
2020-02-29 00:00:00+00:00  180041.82           124393.85                    69.09
2020-03-31 00:00:00+00:00  190745.63           137229.61                    71.94
2020-04-30 00:00:00+00:00   91988.59            68064.36                    73.99

- Extra credit: 773831.3599999713
```

## Problem 2: Data Pulling
We are interested in pulling financial transaction data from a 3rd party API so that we can
perform financial analysis on it. The API provides the transaction data in a JSON format. We
would like to pull fresh data on a weekly schedule. We also know that the number of
transactions produced each week can be large, frequently measured in the millions.

The 3rd party API has a few constraints:
-  Each request has a maximum page size of 100 records
-  The API limits the number of requests using a sliding window such at most
 a 1000 requests can be made every 10 minutes
-  The maximum requests inside the 10 minute window may be less than 1000 if
 the load
on the 3rd party API is high
● If we exceed the maximum number of requests within a 10 minute window, we receive
an HTTP 400 with a corresponding error message.

Once the data is pulled, we also want to provide a way to query the data. Some example
queries that we might want to run are:
- Filter transactions from a start date to an end date
- Filter transactions by particular customers Id’s
-  Perform groupings on sets of customers and transaction dates similar to
 Problem 1.
 
Write 3-4 paragraphs describing how you might design a system that, given these constraints,
can reliably and efficiently pull, store and query the data. This should not be more than one
page. This is an open ended question and there is no ‘right’ answer, however be sure to write
out any assumptions you make. Some questions to consider while designing:

- What are the specific technology choices you would make?
- How would you design around the rate limits of the 3rd party?
- What failure cases are there, and how are they handled?
- Where is the resulting data stored and what, if any, transformations are
 necessary?
 
#### Answer

A micro service responsible for making requests, storing information and providing an access API.

1. To query the information, use __RabbitMQ__ with 2 queues, 1 "request_3pa
" queue for new tasks that involve requesting the 3PA API until you get a 400 error or finish reading all the records. In case of a 400 error, the task is sent to another "request_3pa_delay" queue, with the special header called x-delay that takes an integer representing the number of milliseconds that RabbitMQ should delay the message. That delay is the minutes of the time window. 

    Each task has the current page of the request as a parameter, in such a way that if there is an error, the request can be resumed on the page that was pending.

2. For the information storage I would use __MongoDB__, due to its high writing
 performance. In addition to that I would use the aggregation available for filtering and grouping data (Mongo Atlas service). So it would delegate that execution at the Database level. Which allows me to scale easily. In addition, this type of database gives us flexibility in case the transformation of the data schema is necessary.

3. To dispatch the information, I would use __FastAPI__ to generate 2 access
 points;
- GET transactions by date range and group by customer or date.
- Get transaction by customer ID. FastAPI is asynchronous so it gives good
 performance.