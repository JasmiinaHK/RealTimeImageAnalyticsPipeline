# Real-Time Image Analytics Pipeline

This project demonstrates the development of a real-time system for large-scale image processing using modern technologies:

- **Kafka** – for streaming image paths  
- **OpenCV and YOLOv4-tiny** – for local object detection  
- **Hadoop MapReduce on AWS EMR** – for distributed analysis and result aggregation  
- **Elasticsearch and Kibana** – for indexing and visualizing metadata  

During the pipeline execution, a dataset of 10,000 images was processed. The image paths were streamed using Kafka, images were analyzed locally using the YOLO model and OpenCV library, and then further processed in the cloud via an AWS EMR cluster. The extracted metadata was indexed in Elasticsearch and visualized using Kibana.

---

## Project Documentation

This end-to-end pipeline integrates multiple tools and platforms to enable object detection, metadata generation, cloud-based processing, and real-time search and visualization.

The full technical documentation includes:

- the overall project goal and system architecture  
- a detailed explanation of each individual component  
- file and folder organization  
- instructions for running the system locally and in the cloud  
- a step-by-step guide to executing the entire pipeline  

The full report is available here:  
[Project_Report.pdf](https://github.com/JasmiinaHK/RealTimeImageAnalyticsPipeline/blob/main/Project_Report.pdf)

---

## Dataset Preparation

**Note:** The `images_subset/` folder is intentionally left empty in this repository in order to avoid uploading large files to GitHub (due to size limitations).

To ensure the pipeline works properly, you must manually create the `images_subset/` folder and download the image dataset to your local machine, as described in the report.
