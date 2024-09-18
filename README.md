# mobimap-kotka

Welcome! This site gives an overview over the mobility of the city Kotka in southern Finland in September 2024.

## General

For this purpose, the mobility of pedestrians, cyclists and car drivers was analyzed. This was done at the Sustainable Mobility Hackathon at the [XAMP-University](https://www.xamk.fi/) in Kotka.

The maps were generated by using the [valhalla-routing engine](https://valhalla.github.io/valhalla/) to calculate the route from the center of every hexagon to the new campus of the university in Kotka. All the default values were used, except for a walking speed of 3.6 km/h for pedestrians.

## Legend

The legend is missing on the map. The colors mean the following things:

- Dark green (A): 0-15 minutes travel time.
- Light green (B): 16-20 minutes travel time.
- Yellow (C): 21 - 30 minutes travel time.
- Orange (D): 31-45 minutes travel time.
- Red (E): > 45 minutes travel time.

## Source

To view the source, go to the root of this project: https://github.com/BWIM/mobimap-kotka

## Maps

There are three maps generated. Just click on the link, and they will open up in a new tab. Feel free to download them and use them, as described in the License.

- [Map for pedestrians](https://bwim.github.io/mobimap-kotka/map_walk_smol.html)
- [Map for cyclists](https://bwim.github.io/mobimap-kotka/map_bike_smol.html)
- [Map for car drivers](https://bwim.github.io/mobimap-kotka/map_car_smol.html)

## More

This was an example map generated in a very simple way. More maps are available at the [mobi.mapr](https://mapr.mobi) soon!

The Maps were created by [Pfennig (Marc Le Large)](https://www.linkedin.com/in/pfennig42/).

For more information, follow the [Baden-Württemberg Institute for sustainable mobility](https://bw-im.de).
