# Basic Computer Vision Tasks: Classification, Detection, and Segmentation

Computer vision can be used to understand images in different ways, depending on how much detail is needed. In disaster response, this can help with quickly sorting images, finding damaged areas, or mapping the exact extent of damage. Three common tasks are image classification, object detection, and segmentation.

## 1. Image Classification

Image classification gives a label to the whole image. The model looks at the image as one complete scene and predicts what category it belongs to.

Examples in a disaster setting:
- A satellite image could be classified as showing a flood, wildfire, earthquake damage, or explosion.
- A post-disaster image could be classified as showing severe damage, moderate damage, or limited damage.

This is useful for quick sorting or triage, especially when there are many images to review. However, classification has an important limitation: it does not show where the object or damage is located in the image.

Common metrics: Accuracy, F1-score

## 2. Object Detection

Object detection finds specific objects in an image and draws bounding boxes around them. Unlike classification, it answers both “what is in the image?” and “where is it?”

Examples in a disaster setting:
- Detect damaged buildings in a post-disaster satellite image.
- Detect flooded roads, collapsed structures, or blocked areas.
- Count how many damaged structures appear in a region.

Detection is useful when location matters. In a disaster response setting, it can help teams find damaged buildings, blocked roads, or flooded areas in the image. The limitation is that bounding boxes are still approximate and do not capture the exact shape of the object.

Common metrics: Mean Average Precision (mAP), IoU

## 3. Segmentation

Segmentation gives the most detailed output of the three tasks. Instead of only labeling the image or drawing boxes, segmentation assigns a label to each pixel in the image.

There are two common types:

- Semantic segmentation: labels each pixel by category, such as road, building, water, or debris.
- Instance segmentation: separates individual objects of the same category, such as distinguishing one damaged building from another.

Examples in a disaster setting:
- Mark exactly which parts of an image show flooded roads.
- Separate damaged buildings from intact buildings.
- Map debris-covered areas after an earthquake.

Segmentation is useful when precise measurement is needed. For example, it can help estimate how much land is flooded or what percentage of infrastructure is damaged. The tradeoff is that segmentation is usually more complex and may require more detailed training data.

Common metrics: Mean IoU, Dice Coefficient

## Summary

| Task | Output | Localization | Complexity |
|---|---|---|---|
| Classification | Image-level label | None | Low |
| Detection | Labels + bounding boxes | Approximate | Medium |
| Segmentation | Pixel-level labels | Pixel-precise | High |

In disaster analysis, the best task depends on the goal. Classification can help with quick triage, detection can help locate and count damaged objects, and segmentation can help measure damage more precisely. In practice, these methods can also be combined depending on the available data and the needs of responders.
