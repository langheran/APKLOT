::convert -background #00000080 -pointsize 100 -fill white label:"A" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - example.jpg"[300%%]" seg1.png
::
::convert -background #00000080 -pointsize 100 -fill white label:"B" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - example.true.mask.png"[150%%]" seg2.png
::
::convert -background #00000080 -pointsize 100 -fill white label:"C" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - example.true.mask.overlay.png"[150%%]" seg3.png
::
::convert -background #00000080 -pointsize 100 -fill white label:"D" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - example.pred.mask.png"[150%%]" seg4.png
::
::convert -background #00000080 -pointsize 100 -fill white label:"E" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - example.pred.overlay.png"[150%%]" seg5.png

convert example.jpg"[100%%]" -bordercolor white -border 3 -bordercolor black -border 2 ( -background white -fill black -pointsize 44 label:(a) -trim +repage -bordercolor white -border 10 ) -gravity South -append -bordercolor white -border 10   -gravity South -chop 0x10 seg1.png

convert example.true.mask.png"[50%%]" -bordercolor white -border 3 -bordercolor black -border 2 ( -background white -fill black -pointsize 44 label:(b) -trim +repage -bordercolor white -border 10 ) -gravity South -append -bordercolor white -border 10   -gravity South -chop 0x10 seg2.png

convert example.true.mask.overlay.png"[50%%]" -bordercolor white -border 3 -bordercolor black -border 2 ( -background white -fill black -pointsize 44 label:(c) -trim +repage -bordercolor white -border 10 ) -gravity South -append -bordercolor white -border 10   -gravity South -chop 0x10 seg3.png

convert example.pred.mask.png"[50%%]" -bordercolor white -border 3 -bordercolor black -border 2 ( -background white -fill black -pointsize 44 label:(d) -trim +repage -bordercolor white -border 10 ) -gravity South -append -bordercolor white -border 10   -gravity South -chop 0x10 seg4.png

convert example.pred.overlay.png"[50%%]" -bordercolor white -border 3 -bordercolor black -border 2 ( -background white -fill black -pointsize 44 label:(e) -trim +repage -bordercolor white -border 10 ) -gravity South -append -bordercolor white -border 10   -gravity South -chop 0x10 seg5.png

montage seg2.png seg3.png -tile 1x2 -geometry +0+0 seg_1.png
montage seg4.png seg5.png -tile 1x2 -geometry +0+0 seg_2.png
montage seg1.png seg_1.png seg_2.png -tile 3x1 -geometry +0+0 seg.png