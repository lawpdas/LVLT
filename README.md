# LVLT: Long-term Vision-Language Tracking
We annotate the popular long-term tracking dataset, [LTB50](https://arxiv.org/abs/1804.07056), with dense language descriptions.
Based on this language-annotated dataset, we extend traditional **Long-term visual Tracking (LT)** to **Long-term Vision-Language Tracking (LVLT)**.

## Language Description Annotator
We also provide an annotation toolkit, which is developed with the [tkinter](https://docs.python.org/3/library/tkinter.html) package.
```commandline
python -m lib.gui 
```
![](https://github.com/lawpdas/LVLT/blob/main/screen.jpg)
- `Text Box`: The upper one shows the last description, the lower one is used to annotate the current frame. 
You can fill the lower one with a language description and click the `save` button (or press the `Enter` key).
- key`Ctrl+Up` and `Ctrl+Down` (button`|<` abd `>|`): choose video
- key`Ctrl+Left` and `Ctrl+Right` (button`<` abd `>`): choose frame
- key`Shift+Left` and `Shift+Right` (button`<<` abd `>>`): fast-backward and fast-forward
- key`Alt+Left` and `Alt+Right` (button`@<<` abd `>>@`): to the last description, to the next description
- key`Enter` (button`Save`): save the description of current frame
- key`Delete` (button`Clear`): clear the description of current frame


## Citation
If you find this project useful in your research, please consider cite:
```
@article{DBLP:journals/corr/abs-1804-07056,
  author    = {Alan Lukezic and
               Luka Cehovin Zajc and
               Tom{\'{a}}s Voj{\'{\i}}r and
               Jiri Matas and
               Matej Kristan},
  title     = {Now you see me: evaluating performance in long-term visual tracking},
  eprinttype = {arXiv},
  eprint    = {1804.07056},
}
```

## References
- [**Now you see me: evaluating performance in long-term visual tracking.**]((https://arxiv.org/abs/1804.07056)) <br />
Alan Lukežič, Luka Čehovin Zajc, Tomáš Vojíř, Jiří Matas, Matej Kristan. arXiv, 1804.07056.

## License
LVLT is released under the [GPL-3.0 License](https://github.com/lawpdas/LVLT/blob/main/LICENSE).
