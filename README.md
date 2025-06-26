Retail Sales Bootcamp Project - 2
This project provides hands-on experience in implementing an end-to-end retail sales data pipeline using Google Cloud Platform (GCP) data services. As Data Engineers, we are responsible for ingesting, transforming, and visualizing retail sales data, ensuring data quality through proper validations and adhering to best practices.

Project Overview
The primary goal of this bootcamp project is to build a robust and scalable data pipeline that handles data from various source systems, transforms it into a clean and usable format, stores it in a target database, and enables business intelligence through visualization.

Architecture
The overall architecture for this project is designed using Draw.io. (Please refer to the separate architecture.drawio or similar file for the visual diagram).

Roles
Our role is that of Data Engineers, responsible for the complete implementation of this end-to-end data pipeline within the GCP ecosystem.

Source Systems
Data for our retail sales pipeline originates from three distinct source systems:

API: Extracting real-time or batch data from a HTTP or RESTful API.

CSV: Loading structured batch data from CSV files.

On-Prem SQL Server: Extracting transactional data from an on-premises SQL Server database.

Dataset for Three Tables
The core dataset revolves around three main entities:

Customers: Stores comprehensive customer information.

Products: Contains detailed product specifications.

Sales: Records individual sales transactions.

Data Definition Language (DDL) Samples:
Below are sample DDLs for the source tables. The actual database schemas might include additional fields.

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerName VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    City VARCHAR(50),
    Country VARCHAR(50)
);

-- Products Table
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10,2),
    StockQuantity INT
);

-- Sales Table
CREATE TABLE Sales (
    SaleID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    SaleDate DATE,
    Quantity INT,
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

Sample Data
The sample data for this project can be sourced from:
AI Shop Dataset on Kaggle

GCP Data Lake Storage (Google Cloud Storage - GCS)
Our data lake in GCS is structured into two main layers:

Bronze Layer: This layer stores the raw, ingested data directly from the source systems. No modifications or transformations are applied at this stage, ensuring data immutability and traceability.

Silver Layer: This layer contains cleansed and transformed data. Data in the Silver layer is ready for further analysis and consumption by downstream systems.

Data Transformation
Tool: GCP Dataflow (powered by Apache Beam) is utilized for performing all necessary data transformations, including cleaning, standardization, enrichment, and aggregation. The Python code previously provided demonstrates a part of this transformation logic for PostgreSQL data.

Target System
The final processed and transformed data is stored in a GCP SQL Database (e.g., Cloud SQL for PostgreSQL, MySQL, or SQL Server, depending on the specific implementation). This database serves as the source for reporting and analytical applications.

Data Visualization
Tools: Looker or Tableau is used to create interactive reports and dashboards. These visualizations will enable stakeholders to analyze sales trends, customer behavior, product performance, and other key business metrics.

Data Validations
To ensure data quality and integrity throughout the pipeline, the following validations are implemented:

Row Count Check: Consistency checks are performed to verify that row counts remain consistent before and after significant transformations (e.g., after ingestion into Bronze, and after transformation into Silver).

Pipeline JSON Validation: Ensuring that pipeline configurations (e.g., Dataflow job definitions, Pub/Sub subscriptions) are correctly defined and adhere to expected schemas.

Triggers
Automated triggers are set up to orchestrate the pipeline execution:

Cloud Scheduler + Pub/Sub → Cloud Functions or Dataflow (To RAW): Used for scheduling API calls and ingesting data into the Bronze (RAW) layer of our GCS data lake.

Scheduled Trigger: Employed for periodic ingestion of data from the on-premises SQL Server database.

Project Deliverables
Mentees are expected to upload the following relevant details to their GitHub repository:

SQL Scripts:

DDL (Data Definition Language) scripts for schema creation (Customers, Products, Sales, and the target summary table).

DML (Data Manipulation Language) scripts for populating sample data into the source tables.

Screenshots: Visual evidence of the deployed pipeline, data in GCS layers, database tables, and visualization dashboards.

Documentation:

This README.md file, explaining the project steps, architectural design, key considerations, and implementation details.
