Backs up an honour save file whenever a save happens in Baldur's Gate 3. 

Run concurrently when playing the game to backup.

Currently, it only works with honour mode.

Run with:
```
python ./main.py
```
Select a save on the first load.

To select a new save to monitor:
```
python ./main.py --reselect
```


Todo:
Change execution to bat/shell file to remove the need for:
```
pip install watchdog
```

Maintain only a set number of backups
