# OpenTaiko-Utils
Extra scripts to improve user experience related to OpenTaiko

## osu2tja

### /!\ IMPORTANT NOTE /!\

Converted charts that aren't yours are for personnal use only.

If you want to distribute converted charts from someone else ask for the chart maker authorization first, we don't support content stealling and strictly condemn it.

### General informations

Based on delguoquing script https://github.com/delguoqing/osu2tja

This osu2tja version aims to fix the multiple bugs contained within the original one, through few bugs are still yet to be patched.

- Language : Python 2

- Usage :
```
python osu2tja.py [[file] [diff]] ...
        diff sets :
                osu2tja [oni[file] [diff]] (Oni only set)
                osu2tja [oni[file] [diff]] [ura oni[file] [diff]] (Oni + ura set)
                osu2tja [oni[file] [diff]] [muzukashii[file] [diff]] [futsuu[file] [diff]] [kantan[file] [diff]] (Regular set)
                osu2tja [oni[file] [diff]] [ura oni[file] [diff]] [muzukashii[file] [diff]] [futsuu[file] [diff]] [kantan[file] [diff]] (Regular + ura set)
```

- Examples :

```
# Oni only set, 8 stars
python osu2tja.py Oni.osu 8
# UraOmote set, Oni 6 stars Ura 9 stars 
python osu2tja.py Oni.osu 6 Ura.osu 9
```