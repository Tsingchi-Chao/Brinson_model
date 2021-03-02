# Brinson_model
The model of Brinson can be used to analyze the return of portfolio or fund.

## Brinson_single_period.py
* Brinson_single_period.py provides a tool named BFModel to analyze the excess return of a fund or your own portfolio by decomposing the excess return into allocation return(by allocating 
the assets like equity,bond,commodity or cash) and selection return(after you allocate the asset like equity,then you will select the the stock and that will bring excess return,too).

* You shold notice that before you use  BFModel you should wash the origin data and get the weight-return matrix.The index is the asset,like cash,equity,bond,commodity or sector
,the columns are"return_bench,return_portf,weight_bench,weight_portf",the return is the return during the period between the date and next date.

## Brinson_mutiple_period.py
* Brinson_mutiple_periods.py provides a tool name AKHModel to analyze the excess return just like that of the BFModel. 

* The main difference is that the BFModel is used to do the analysis in a single peroid but AKHModel is used to do analysis in mutiple periods.
