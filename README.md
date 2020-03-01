# Compliance-content-nz VersionChange (increment Version no.)

## env

* For mac version need to install `python3` 

This can be done by 

```
>> brew install python3
```

* For windows version 

The python3 env have already been packed and all in dist and build folder

It can be run directly


## How To Run

This script is for increasing all the version of compliance-content-nz by one

This includeing all the version under `Releases` folder and all the `tags.yml` files version

Open the terminal

```
>> cd VersionChange
>> py checkVersion_windows.py <your root absoulte path of `compliance-content-nz` in your local drive>
```
Example 

```
>> python3 checkVersion_windows.py /Users/steven.liu/Desktop/MYOB/compliance-content-nz
```
if you want increament all the version add `-i`  flag behind

```
>> python3 checkVersion_windows.py /Users/steven.liu/Desktop/MYOB/compliance-content-nz -i
```
# Compliance-content-nz errormapping

Please check the format before using the script, the format need to be same as errors.xlsx

## how to run 
```
 python3 autoMapping.py <year> <the absoult path to your compliance-content-nz>
```
Example

```
>> python3 autoMapping.py 2020 /Users/steven.liu/Desktop/VersionChange/ErrorMapping/compliance-content-nz
```
