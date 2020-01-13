# Photography-Organizer
Command-line application to help reduce photography's organization time consumption.

## Getting Started

### Prerequisites
[exifread](https://github.com/ianare/exif-py)
```
pip3 install exifread
```

## Running the tests

## Commands
 * rn
   * -h >> Show help message.
   * -d >> Desired directory. If no directory is specified, the current directory is used.
   * -p >> Desired prefix.
   * -v >> Desired start renaming value. If no value is specified, the renaming process will follow a numerical pattern.
 
 ```
phorg rn [-h] [-d] [-p] [-v]
```
 
 * org
   * organization_method >> Parameter through which the content will be organized.
     * day
     * month
     * year
     * shutter_speed
     * lens
     * aperture
     * ISO
     * focal_length
   * -h >> Show help message.
   * -d >> Desired directory. If no directory is specified, the current directory is used.
   * -f >> Name of the main folder where the organized folders will be stored. If no name is specified then a default name is used ('organized_by_<organization_method>')

```
phorg org [organization_method] [-h] [-d] [-f]
```


