# Comparaison de l'annotation protéique d'alpha-cyanobactérie par un model reposant sur les réseaux de neurones profonds et par InterProScan 

![Image](https://github.com/user-attachments/assets/afb9f125-205f-4c3c-8d2c-4cfdd300f3ec)
## Description du projet

Les PicoCyanobactéries, sont les plus petits et les plus abondants micro-organismes photosynthétiques présents sur Terre, leur étude est donc essentielle pour appréhender les diverses relations écologiques se déroulant en milieu marin.

Cyanorak<sup>1</sup> est un outil de bio-informatique dédié à la conservation, la comparaison et la visualisation des génomes de Picocyanobacteria. Il permet une meilleure compréhension de l’écologie, la physiologie et l’évolution de ces organismes.

L’annotation fonctionnelle permet, par la comparaison de séquences d'intérêts à des séquences déjà annotées, de repérer la présence de motifs spécifiques à certaines fonctions biologiques.

L’annotation de séquences protéiques courantes se réalise grâce à des banques de domaines comme InterPro<sup>2</sup>, Pfam<sup>3</sup> ou Gene Ontology<sup>4</sup>. 
Cependant, malgré ces banques de domaines, il reste de nombreuses protéines non annotées.

Chaque année, de nombreux outils reposant sur des réseaux de neurones profonds voient le jour. 

Notre objectif est de comparer PLMsearch<sup>5</sup> et InterProScan sur l’annotation protéique des séquences d’α-cyanobactérie, peu ou mal annoté de Cyanorak.

## Prérequis

- Connaissance de base en biologie moléculaire.
- Familiarité avec les bases de données biologiques.
- Savoir utiliser Python, Github et un tableur 
- Connaissance succinte d'un modèle de deep learning (embeding space, K-mer, etc.)

## Outils et technologies

- PLMsearch[https://github.com/maovshao/PLMSearch]
- Python pour l'analyse de données
- Accès aux bases de données UniProt et Interpro

## Résultats attendus

Nous devront fournir un poster scientifique avec:
- Une analyse des résultats fournit par le model utilisé par rapport au prédiction d'InterProScan
- Une analyse critique des résultats et des limites des méthodes utilisées.
- Une présentation synthétique des travaux sous forme orale ou écrite.

 Dorian LE ROUX lerouxdorian.pro@gmail.com & Emile HEMBERT emile.hembert@gmail.com - Etudiant licence 2 BioMAD SU - Station biologique de Roscoff
 
 Encadrement : Juliana Silva Bernardes (UMR7144, juliana.silva_bernardes@sorbonne-universite.fr) et Laurence Garczarek UMR7144, laurence.garczarek@sb-roscoff.fr)

<sup>1</sup> Garczarek et al. Nucleic Acids Research, 2021. https://doi.org/10.1093/nar/gkaa958

<sup>2</sup>  Matthias Blum & al. InterPro: the protein sequence classification resource in 2025, Nucleic Acids Research, Volume 53, Issue D1, 6 January 2025, Pages D444–D456,      
              https://doi.org/10.1093/nar/gkae1082
<sup>3</sup> Pfam: The protein families database in 2021: J. Mistry, S. Chuguransky, L. Williams, M. Qureshi, G.A. Salazar, E.L.L. Sonnhammer, S.C.E. Tosatto, L. Paladin, S. Raj, L.J. 
 <sup>4</sup>Richardson, R.D. Finn, A. Bateman, Nucleic Acids Research (2021) doi: 10.1093/nar/gkaa913
             Ashburner et al. Gene ontology: tool for the unification of biology. Nat Genet. 2000 May;25(1):25-9. DOI: 10.1038/75556
<sup>4 bis</sup>The Gene Ontology Consortium. The Gene Ontology knowledgebase in 2023. Genetics. 2023 May 4;224(1):iyad031. DOI: 10.1093/genetics/iyad031
<sup>5</sup> Liu, Wei, et al. Nature communications, 2024. https://doi.org/10.1038/s41467-024-46808-5
