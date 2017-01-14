# Weblogic config.xml parse

### Desc

This is weblogic config.xml parse program

### Usage

For command line, need install Python3 and **Paramiko**

```bash
./command.py -t 10.0.0.0 -u root -p root
```

For docker command line

```
docker run --rm -v YOUR_VOL:/data/file playniuniu/weblogic-cmd -t 10.0.0.0 -u root -p root
```

### Update config file

edit config.xml file and use command with **-w** option

```
./command.py -t 10.0.0.0 -u root -p root -w
```
