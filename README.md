# Popular Unserved Routes

## Overview

Hi, avgeek (aviation enthusiast) and someone curious to explore passenger flows on flights throughout the U.S. here :D

This program analyzes 2024 Bureau of Transportation Statistics data (from the U.S. government) to identify the most popular destination airports from a user-entered origin airport that are not served by a nonstop flight

I was intrigued by some of the results after running this analysis on a bunch of airports, especially my home airports, leading me to try to figure out why there isn't a nonstop flight between ABQ and LGA (well that one's pretty easy... see [LaGuardia Airport's perimeter rule](https://en.wikipedia.org/wiki/LaGuardia_Airport#:~:text=Also%20in%201984%2C%20to%20further%20combat%20overcrowding,became%20the%20only%20exception%20to%20the%20rule.))

Anyway, have fun trying this out with your home airport!

## Data Sources

- [BTS DB1B Market table for quarters 1-4 of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFI&Yv0x=D)
  -  For passenger flow data


- [BTS T-100 Domestic Segment table for all of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE)
  - For finding airport pairs connected with a nonstop flight

## Tools

- Python


- pandas


- matplotlib

This is kind of a rudimentary program at the moment, but I have some ideas for expansion

Speaking of which...

## Ideas for Expansion

- Allowing the graph to show both served and unserved routes with a color-coded bar chart


- Providing an option to save an image of the graph made


- Moving this out of the console... maybe

## Limitations

Obviously there are some limitations that come out of analyzing only two datasets...

- The data is not real-time; it comes from BTS data tables that the government releases only once a quarter


- This analyzes 2024 data because that is the most recent year with a full year of data
  - There's a 6-month delay for when the government makes the DB1B tables available to the public

    
- This does not include any airport pairs with an airport outside the U.S. because the DB1B tables only have American airports


- City pairs with seasonal flights are excluded because they will show up in the T-100 at some point for the year, even if flights are not operated during every month


- You should probably be cautious with using solely this analysis to determine whether an airline to start new routes because the number of passengers traveling between two airports is just one piece of the network planning puzzle
  - Also must consider _fares_, premium demand, seasonality, operational constraints, aircraft availability, etc.