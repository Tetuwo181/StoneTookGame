# StoneTook
- 石取りゲームを実行するプログラムです
- 記録を残した後、別途データを学習させ、戦えるようにします

# 構成
module/<br>
├ field/<br>
| 　　 ├__init__.py<br>
| 　　 ├battle_data_builder.py<br>
|  　　├nim.py<br>
|  　　└sample.py<br>
├ player/<br>
|  　　├strategies/<br>
|  　　|  　├__init__.py<br>
|  　　| 　 ├one_took.py<br>
|  　　| 　 ├random.py<br>
|  　　|  　└strongest.py<br>
|  　　├__init__.py<br>
|  　　├player.py<br>
|  　　└sample.py<br>
└ recorder/<br>
  　　├__init__.py<br>
  　　├data_loader.py<br>
  　　└recorder.py<br>
