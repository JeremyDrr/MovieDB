# Movie Search Application

## Overview

The goal of this project is to propose a fluid and seamless experience for movie browsing through a vast database of audiovisual content.

## Technology stack

- **Python 3.X**
- **Elasticsearch**
- **Flask**
- **CSV**

## REST API

<h3 style="text-align: center;">CRUD operations</h3>

| METHOD     | ROUTE                           | DESCRIPTION                       |
|------------|---------------------------------|-----------------------------------|
| **POST**   | `/api/create/`                  | Add a new movie                   |
| **GET**    | `/api/movies/{movie_id}`        | Get a specific movie by its ID    |
| **PUT**    | `/api/movies/update/{movie_id}` | Update a specific movie by its ID |
| **DELETE** | `/api/movies/delete/{movie_id}` | Delete a specific movie by its ID |


## Installation

1. Download `Elasticsearch` client for Windows
2. Extract the ZIP folder
3. Download the project folder
4. Extract the project ZIP folder
5. Download the CSV of dataset at this [link](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
6. Copy the downloaded CSV at the root of the project folder

## Elasticsearch Mappings

<img src="https://github.com/JeremyDrr/MovieDB/blob/main/Elasticsearch_mappings.png" width="200">

