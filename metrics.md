# Evaluation Metrics

This document defines the metrics used to evaluate the quality of food weight predictions made by the model.
In the context of visually estimating food weights from images, different types of errors have different impacts depending on the food's size. To capture these nuances, we use three complementary metrics: MAE, MAPE, and Weighted MAE.

## 1. Mean Absolute Error (MAE)
MAE gives an intuitive measure of how far, on average, predictions are from ground truth values in absolute grams. It treats each food item equally, regardless of its weight.

$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^n \left| \hat{y}_i - y_i \right|
$$

- $\hat{y}_i$: predicted weight (in grams) 
- $y_i$: ground truth weight
- $n$: total number of food items

Pros:
- Intuitive and easy to interpret

Cons: 
- Treats all errors equally regardless of context, a 10g error on a 20g food is as bad as a 10g error on a 200g food.

## 2. Mean Absolute Percentage Error (MAPE)
MAPE captures the relative error, helping assess whether the prediction is proportionally close to the true value. For instance, overestimating a 30g food by 30g is more problematic than overestimating a 300g item by 30g.

$$
\text{MAPE} = \frac{100}{n} \sum_{i=1}^n \left| \frac{\hat{y}_i - y_i}{y_i} \right|
$$

Pros: 
- Normalizes errors by food size, enabling fairer comparison across items of varying weights
- Highlights large relative errors on small foods

Cons: 
- Unstable when $y_i$ is close to zero 
- Overly penalizes small absolute errors on small items, for example a 3g error on a 1g tiem leads to a 300% MAPE

## 3. Weighted MAE
Weighted MAE increases the impact of errors on heavier food items by multiplying each absolute error by the item’s true weight. This gives more influence to high-weight foods in the final score. Finally, it is normalized by the total weight of the whole dish to ensure the total contribution is proportional to the dish weight.  

### Per-dish Weighted MAE
Given a dish composed of multiple food items $i \in \{1,..,m\}$ each with a true weight $y_i$ and predicted weight $\hat{y}_i$, the per-dish Weighted MAE is:

$$
\text{Weighted MAE}_{\text{dish}} = \frac{\sum_{i=1}^{m} \left| \hat{y}_i - y_i \right| \cdot y_i}{\sum_{i=1}^{m} y_i} 
$$

This formula:
- Weighs the error for each food item by its actual weight
- Normalizes by the total weight of the dish
- Reflects how important each item's accuracy is in the context of the whole dish


**Remark**: It is important to note that when evaluating the model on a subset of the data, the full dish composition is not always available. In such cases, the Weighted MAE is computed over the available food items only, using the same per-dish formula, where $m$ is the number of items in the sample. This ensures that the metric remains meaningful even when dishes are only partially annotated or evaluated.


### Total Weighted MAE (applicable only on full dataset)
To summarize performance across multiple dishes, we compute the mean of all per-dish Weighted MAEs:

$$
\text{Total Weighted MAE} = \frac{1}{D} \sum_{i=1}^D \text{Weighted MAE}_{\text{dish i}}
$$

Where $D$ is the number of dishes in the dataset.

Pros: 
- Gives more importance to error on larger items
- Reflects meal-level impact

Cons: 
- Treats all dishes equally, regardless of how many food items they contain or how large they are


## Summary

**MAE** gives a raw understanding of typical errors in grams.  
**MAPE** contextualizes these errors relative to each food's size.  
**Weighted MAE** focuses on evaluating entire meals where accuracy of high-weight items is most critical.

Together, they offer a comprehensive view of the model’s strengths and weaknesses in estimating the volume of food from images.