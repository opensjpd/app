# OpenSJPD

OpenSJPD aims to provide transparency to San José Police by way of data analysis. 
We believe that more transparency in government leads to better accountability and, ultimately, better and more equitable outcomes.
All analysis we do is in the spirit of improving safety and equity for all.

## Data
All data comes (directly or indirectly) from records requests with the relevant government agencies.
The quality of our analysis is only as good as the data we have. There are some limitations to the data we have (see "Known Limitations" below). 

## Errors
While we make every effort to ensure our analysis is correct, errors are possible. 
If you spot an error in our analysis, [please email us](mailto:data@opensjpd.com) or open a [Github issue](https://github.com/opensjpd/app/issues) so we can fix it.
In the spirit of openness, our code and the underlying datasets are available to view.

## Licensing
The raw datasets are public records. If you decide to use or distribute them, we would appreicate you attributing them to **OpenSJPD**.  
Commercial usage of the code contained in this repository is *expressly forbidden*. Government usage of the code is subject to case-by-case approval. 
Non-profit use of our code is *strongly encouraged* and only requires that the project attributes OpenSJPD. 
Please [email us](mailto:data@opensjpd.com) if you have any questions.

## Known Limitations

* The arrest datasets are missing the "arresting officer" field for about 30% of arrests. This field is more frequently filled in more recent records.
* Subjects' race may not be correctly or consistently reported, and could vary between repeat arrests.
* There is also no option for multiracial or multiethnic people.
* SJPD only records "Male" or "Female" for subjects, and does not take into account the spectrum of gender identities or the existence of intersex people.
* "Reason for arrest" fields are not standardized. Typos and abbreviations make it difficult to generate statistics. For example, `POSSESS CONTROLLED SUBSTANCE` versus `POSSESS CNTLD SUBSTANCE`.
* Some arrests are recorded as multiple rows in the "Arrests" table if there are multiple charges. This makes it difficult to determine how many true arrests an officer has made.
