convert -background #00000080 -pointsize 100 -fill white label:"A" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+50 - 11_thumb.jpg"[300%%]" seg1.png

convert -background #00000080 -pointsize 100 -fill white label:"B" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+50 - 11_object_thumb.png"[300%%]" seg2.png

convert -background #00000080 -pointsize 100 -fill white label:"C" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+50 - 11_class_thumb.png"[300%%]" seg3.png

montage seg1.png seg2.png seg3.png -tile 3x1 -geometry +0+0 seg.png
convert seg.png -gravity North -chop 0x45 seg.png
convert seg.png -gravity South -chop 0x45 seg.png