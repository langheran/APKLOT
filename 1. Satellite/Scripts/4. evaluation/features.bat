convert -background #00000080 -pointsize 100 -fill white label:"A" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +20+70 - size-stats.png"[100%%]" feat1.png

convert -background #00000080 -pointsize 100 -fill white label:"B" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +40+70 - width,height-stats.png"[100%%]" feat2.png

convert -background #00000080 -pointsize 100 -fill white label:"C" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +40+70 - total_area,area-stats.png"[100%%]" feat3.png

convert -background #00000080 -pointsize 100 -fill white label:"D" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +20+70 - area_count-stats.png"[100%%]" feat4.png

montage feat1.png feat2.png feat3.png feat4.png -tile 4x1 -geometry +0+0 features.png
convert features.png -gravity North -chop 0x60 features.png
convert features.png -gravity South -chop 0x15 features.png