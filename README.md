# q3_railgun_patch
`change_cooldown.py` will help you change q3 railgun cooldown time without recompiling `qagame.qvm`.

## usage
```bash
python3 change_cooldown.py /path/to/vm/qagame.qvm "${NEW_TIME_IN_MS}"
```
or
```bash
python3 change_cooldown.py /path/to/vm/qagame.qvm "${NEW_TIME_IN_MS}" "${OLD_TIME_IN_MS}"
```
`OLD_TIME_IN_MS` is `1500` by default (as in the original `Q3A` game).

## disclaimer
Please respect copyrights. Remember, if you patching binaries without source code and/or proprietary, law-protected - author has nothing to do with it.

## implementation details
- patch target translation unit: `code/game/bg_pmove.c`, function: `PM_Weapon`
- patch target code:
  - https://github.com/ioquake/ioq3/blob/3fb9006e6461b877b67781cd0f0d94032804a475/code/game/bg_pmove.c#L1669
  - https://github.com/id-Software/Quake-III-Arena/blob/dbe4ddb10315479fc00086f08e25d968b4b43c49/code/game/bg_pmove.c#L1670
  ```c++
  case WP_PLASMAGUN:
    addTime = 100;
    break;

  case WP_RAILGUN:
    addTime = 1500; /* <-- we need to change this */
    break;

  case WP_BFG:
    addTime = 200;
    break;
  ```
- `qvm` binary pattern (generated via `ioquake3` assembler)
  ```
  0000 2008 1621 0100 0a09 0c00 0000 08 ; prefix
  dc 05 ; <-- we need to change this
  00 0020 0816 2101 000a 090c 0000 0008 ; suffix
  ```

- `qvm` assembler code:
  ```assembler
  LABELV $619
  ADDRLP4 0
  CNSTI4 100
  ASGNI4
  ADDRGP4 $611
  JUMPV

  LABELV $620
  ADDRLP4 0
  CNSTI4 1500 ; <-- we need to change this
  ASGNI4
  ADDRGP4 $611
  JUMPV

  LABELV $621
  ADDRLP4 0
  CNSTI4 200
  ASGNI4
  ADDRGP4 $611
  JUMPV
  ```
