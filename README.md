# Popular Unserved Flight Routes

## Overview

Hi, avgeek (aviation enthusiast) here! Just curious to explore popular unserved flight routes in the U.S. commercial aviation network. ✈️

### What this does

This rather simple project analyzes 2024 Bureau of Transportation Statistics data (from the U.S. government) to identify the most popular destination airports from a user-entered origin airport that lack nonstop flights.

### Why I made this

I've always been fascinated in airline route networks and passenger flows across the system, especially where they do not align. While passengers might connect for price, schedule, or to [visit ORD for fun like I did](https://my.flightradar24.com/kin_on_a_plane), popular airport pairs without nonstop service _may_ present an important market opportunity. (Of course, the passenger count is just one of many factors in network planning.)

### What I learned from this

Running this analysis on my home airports revealed interesting hidden markets I hadn't considered. Without this, I never would've known that the top unserved airport from ABQ is LGA, where, in 2024, over 38,000 passengers connected to reach the Big Apple. (But any frequent flyer would know that [LaGuardia's perimeter rule](https://en.wikipedia.org/wiki/LaGuardia_Airport#:~:text=Also%20in%201984%2C%20to%20further%20combat%20overcrowding,became%20the%20only%20exception%20to%20the%20rule.) prevents nonstop service from existing, at least on six days of the week.)

**Give it a run with your home airport to see the hidden markets you might find!**

## Data Sources

- [BTS DB1B Market table for quarters 1-4 of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFI&Yv0x=D)
  -  For passenger flow data


- [BTS T-100 Domestic Segment table for all of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE)
  - For identifying airport pairs connected with a nonstop flight

## Tools

- Python

- pandas

- matplotlib

- Tkinter

## Limitations

Obviously there are some limitations that come out of analyzing only two datasets:

- You should probably be cautious with using solely this analysis to determine whether an airline should start new routes because the passenger count is just one piece of the network planning puzzle
  - Also must consider fares, _premium_ demand, seasonality, operational constraints, aircraft availability, etc.


- The data is not real-time; it comes from BTS data tables that the government releases only once a quarter


- 2024 data is analyzed because that is the most recent year with a full year of data
  - There's a 6-month delay for when the government makes the DB1B tables available to the public


- The exact passenger count is unknown because the DB1B tables are only a random 10% sample of tickets, so DB1B counts are multiplied by 10 to approximate the actual count

    
- Routes with an airport outside the U.S. are excluded because the DB1B tables only have American airports


- City pairs with seasonal flights are excluded because they will show up in the T-100 at some point for the year, even if flights are not operated during every month


- Airports with no scheduled, commercial service in 2024 but _may_ have demand are excluded because it's not possible to book a flight out of those airports (and have a record on DB1B tables)