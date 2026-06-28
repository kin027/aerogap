# AeroGap
Airline Nonstop Service Gap Identifier

## Overview

A Python data analysis tool that identifies the most popular destination airports from a user-entered origin airport that lack nonstop flights using 2024 Bureau of Transportation Statistics (BTS) data.

### Why I made this

Alright, so I'm an avgeek (aviation enthusiast) and data nerd. In [my 300,000+ miles at cruising altitude](https://my.flightradar24.com/kin_on_a_plane), I always wondered where the other passengers on my flights connected to/from if they didn't fly nonstop to their final destinations. That curiosity grew into exploring potential gaps in nonstop service from the airports I frequented. 

Side note: Even if nonstop service existed, I would still connect for fun :D

Also, routes are at the heart of airlines, as their route networks can make or break their bottom lines. Popular O/D (origin/destination) pairs without nonstop service _may_ present an important market opportunity to them. (But of course, the passenger count is just one of many factors in network planning.)

### What I learned from this

Running this analysis on my frequented airports revealed interesting nonstop service gaps I hadn't considered. Without this, I never would've known that the top unserved airport from PDX (Portland, OR) is MSY (New Orleans), where, in 2024, over 39,000 passengers connected to reach the Big Easy. (And Alaska Airlines probably knew too, seeing as they [started seasonal service between the two in 2025](https://news.alaskaair.com/loyalty/alaska-airlines-launches-seasonal-daily-flight-between-portland-and-new-orleans/).)

**Give it a run with your home airport to see its nonstop service gaps!**

## Getting Started

Make sure you have Python 3.13 or higher installed. 

Note for Linux users: You may need to install Tkinter manually if it isn't included in your distro's default Python package:
```bash
sudo apt-get install python3-tk
```

1. Clone this repository:
```bash
git clone https://github.com/kin027/popular-unserved-flight-routes.git)
cd popular-unserved-flight-routes
```

2. Create a virtual environment:
```bash
# Create the environment
python -m venv venv

# Activate it:
# On macOS and Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```
3. Install the dependencies (you don't need to download the datasets themselves as I've already included the final ones in the repo):
```bash
pip install -r requirements.txt
```
4. Run the program!
```bash
python main.py
```

## Data Sources

I sourced data from the Bureau of Transportation Statistics (BTS), which is reported by airlines to the U.S. government.

- [BTS DB1B Market table for quarters 1-4 of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFI&Yv0x=D) (to get passenger flow data)

- [BTS T-100 Segment (All Carriers) table for all of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE) with DepScheduled, Passengers, UniqueCarrierName, Origin, Dest, Year, Class fields (to identify airport pairs connected with a nonstop flight)

## Libraries Used

- pandas (to comb through the T-100 and DB1B tables)

- matplotlib (to create the visualization)

- Tkinter (to implement the GUI)

## Limitations

Obviously there are some limitations that come out of analyzing only two datasets:

- You should probably be cautious with using solely this analysis to determine whether an airline should start new routes because the passenger count is just one piece of the network planning puzzle.
  - Other factors to consider include fares, _premium_ demand, seasonality, operational constraints, aircraft availability, etc.

- The data is not real-time; it comes from BTS data tables that the government releases only once a quarter (with a six-month delay).
  - 2024 data is analyzed because that is the most recent year with a full year of data.

- The exact passenger count is unknown because the DB1B tables are only a random 10% sample of tickets, so DB1B counts are multiplied by 10 to approximate the actual count.
    
- Routes with an airport outside the U.S. are excluded because the DB1B tables only have American airports.

- City pairs with seasonal flights are excluded because they will show up in the T-100 at some point for the year, even if flights are not operated during every month.