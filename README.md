# Load-Prediction
### Note: the codes are jupyter notebooks, if you have problems opening it, please use [nbviewer](https://nbviewer.jupyter.org/)

Predicting peak loads for electricity grid. We have 2 data sets: a high resolution (half-hourly) and a low resolution (~few times a year) data sets. We want to make daily peak-load predictions for the low resolution data set based on the knowledge of the high resolution data.

Note: the data sets publised here, are only the head 10 rows of the original files added some noise on it because of data privacy issue.

## Step 01 - Data Cleaning
The above mentioned low resolution data needs some preparation before processing. The data set is full of null values, real data can be found at only few points. For this reason we need to clean it. First delete all rows with no data points at all. (If we have only NaN values in a row, then we drop that row.) We save the result to "CleandFromAllNull.xlsx".

After clearing the all-NaN rows we interpolate the rest. If we have 2 points with value and NaN-s between, we assume steady consumption there. On the other hand the input data set has aggregated data (how much electricity has been used until the actual time point) but we need electricity useage in every half-hour time interval (not aggregated).
Eg.

|day1 |day2 |day3|day4|day5 |day6|... |
| --- | --- | - | --- | --- | - |---  |
|NaN  |NaN  |**3**|NaN  |NaN  |**6**|...  |

Here we start with NaN-s, so until the first value we change all NaN-s to 0-s. After the first value (**3**) we have 2 more NaN-s and then the second value (**6**). Now we assume steady consumption between our **3** and **6**. The difference between the values is **6-3** = 3, this 3 value is for 4 days (day3, day4, day5, day6) so the portion of each time-interval is 3/4 = 0.75.
The above example data will be processed like:

|day1 |day2 |day3|day4|day5 |day6|... |
| --- | --- | -- | -- | --- | -- |---  |
|0  |0  |**3.75**  |0.75  |0.75 |**0.75**|...  |

Now we have our test data ready.

## Step 02 - Create Clusters
We need to order our learning data to clusters. When we have the clusters we can count for each test data the closest cluster. Then based on the learning data in that cluster we can make peak load predictions for our test data.

The make it possible to count distance between our clusters and test data, the dimension of the test data and the vectors in the cluster must be equal. As the test data has lower dimension (it's resoultion is daily not half-hourly) first we need to reduce the resolution of the half-hourly learning data to become daily. Note: we need to keep the original resolution as well for the peak load predicitons later.

After we reduced the resolution we can create clusters. We use [spectral clustering](https://towardsdatascience.com/spectral-clustering-aba2640c0d5b) to cluster it. The number of clusters needs to be set in the program, usually the less than 10 is a good chice.
Note: the project could be improved by trying different number of clusters, finding the number with best accuracy.

After clustering the reduced dimension learning data vectors. Count the average of vectors in each cluster, creating a cluster-center vector. At this point we can start using the prepared test data.

For each test data vectors we count the distance between the cluster-center vectors. We group each test data vectors to the closest cluster. And based on the (high resolution version of) learning data vectors in the cluster we can give half-hourly load prediction to the low resolution learning data vectors.
