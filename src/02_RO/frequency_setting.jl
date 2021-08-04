"""
This is the julia script for frequency setting problem
"""

using DataFrames, CSV
using Dates

cd("/Users/xiaotong/Documents/GitHub/transit-centric-smart-mobility-system/")

println("Robust Optimization Module is successfully run")

# sample outputs
dispatching_time_list = []
dispatch_tt = Time(7,0,0)
while dispatch_tt <= Time(10,0,0)
    global dispatch_tt
    push!(dispatching_time_list, dispatch_tt)
    dispatch_tt += Minute(5)
end

output_dispatching_time_list = []
for i in dispatching_time_list
    push!(output_dispatching_time_list, Dates.format(i, "HH:MM:SS"))
end

CSV.write("data/02_INTERMEDIATE/dispatching_time.csv", (; time = output_dispatching_time_list))
