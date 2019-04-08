-- WordNets. Catalan, English, Basque, Galician, Portuguese and Spanish

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/spaWN/wei_spa-30_examples.tsv' INTO TABLE `wei_spa-30_examples`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/spaWN/wei_spa-30_relation.tsv' INTO TABLE `wei_spa-30_relation`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/spaWN/wei_spa-30_synset.tsv' INTO TABLE `wei_spa-30_synset`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/spaWN/wei_spa-30_to_ili.tsv' INTO TABLE `wei_spa-30_to_ili`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/spaWN/wei_spa-30_variant.tsv' INTO TABLE `wei_spa-30_variant`;

-- AdimenSUMO

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/AdimenSUMO/wei_ili_to_sumo.tsv' INTO TABLE `wei_ili_to_sumo`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/AdimenSUMO/wei_sumo_relations.tsv' INTO TABLE `wei_sumo_relations`;

-- BLCs

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/BLC/wei_ili_to_blc.tsv' INTO TABLE `wei_ili_to_blc`;

-- data

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/data/wei_ili_record.tsv' INTO TABLE `wei_ili_record`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/data/wei_lexnames.tsv' INTO TABLE `wei_lexnames`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/data/wei_relations_group.tsv' INTO TABLE `wei_relations_group`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/data/wei_relations.tsv' INTO TABLE `wei_relations`;

-- Domains

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/Domains/wei_domains.tsv' INTO TABLE `wei_domains`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/Domains/wei_ili_to_domains.tsv' INTO TABLE `wei_ili_to_domains`;

-- Marks

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/Marks/mark_values_synset.tsv' INTO TABLE `mark_values_synset`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/Marks/mark_values_variant.tsv' INTO TABLE `mark_values_variant`;

-- Top Ontology

LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/TopOntology/wei_ili_to_to.tsv' INTO TABLE `wei_ili_to_to`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/TopOntology/wei_to_record.tsv' INTO TABLE `wei_to_record`;
LOAD DATA LOCAL INFILE '/home/imart02/tfg-analogias/TFG-1819-Analogias/PruebaPrototipo/mcr30-2016/TopOntology/wei_to_relations.tsv' INTO TABLE `wei_to_relations`;
