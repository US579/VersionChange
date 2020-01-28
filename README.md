# compliance-content-nz VersionChange

## env

This script is for increasing all the version of compliance-content-nz by one

This includeing all the version under `Releases` folder and all the `tags.yml` files version

* For mac version need to install `python3` 

This can be done by 

```
>> brew install python3
```

* For windows version 

The python3 env have already been packed and all in dist and build folder

It can be run directory


## How To Run


####  Mac

Open the terminal

```
>> cd VersionChange
>> python3 changeVersion.py <your root absoulte path of compliance-content-nz>
```

#### windows 

Open the terminal

```
>> cd VersionChange
>> cd dist
>> ./changeVersion <your root absoulte path of compliance-content-nz>
```




