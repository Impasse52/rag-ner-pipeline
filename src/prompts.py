# [OBSOLETE]
old_ner_prompt = """Sono un eccellente linguista, specializzato nel rintracciare entità in testi giuridici. Il mio compito è di etichettare usando BIO tagging tutte le entità nominate in un testo come segue:

- le persone sono etichettate tra doppie parentesi tonde: ((PER))
- i luoghi sono etichettati tra doppie parentesi quadre: [[LOC]]
- le organizzazioni sono etichettate tra doppie parentesi graffe: {{ORG}} 
- le misc sono etichettate tra doppie parentesi angolari: <<MISC>>

Ecco alcuni esempi:


Input: Del resto l’atteggiamento di colpevole condivisione della stra tegia stragistica voluta dal Luca Rinaldi anche per l’eliminazione del dr Paolo Conti era provata non solo dal ruolo preminente che Andrea Moretti aveva continuato a rivestire nell’organizzazione anche dopo l’attentato di Marina Alta, alla luce dalle dichiarazioni di tutti i colla boranti ancora in libertà all’epoca, ma anche dalla sua partecipazione all’incontro nel quale circa un mese dopo la strage il Luca Rinaldi aveva fe steggiato in casa del Francesco Villa con un brindisi, in sieme a Alessandro Greco, Riccardo Galli, Stefano Romano, Davide Marchetti ed appunto il Andrea Moretti, la riuscita del barbaro crimine.
Output: Del resto l’atteggiamento di colpevole condivisione della stra tegia stragistica voluta dal ((Luca Rinaldi)) anche per l’eliminazione del dr ((Paolo Conti)) era provata non solo dal ruolo preminente che ((Andrea Moretti)) aveva continuato a rivestire nell’organizzazione anche dopo l’attentato di [[Marina Alta]], alla luce dalle dichiarazioni di tutti i colla boranti ancora in libertà all’epoca, ma anche dalla sua partecipazione all’incontro nel quale circa un mese dopo la strage il ((Luca Rinaldi)) aveva fe steggiato in casa del ((Francesco Villa)) con un brindisi, in sieme a ((Alessandro Greco)), ((Riccardo Galli)), ((Stefano Romano)), ((Davide Marchetti)) ed appunto il ((Andrea Moretti)), la riuscita del barbaro crimine.

Input: MESSINA Leonardo ha riferito che la commissione regionale di Consorzio Civico Tirrenico era costituita tra i rappresentanti delle province di Castelvento, Rocca Serena, Pian del Lago, San Felice al Piano, Monteluce e Colle Azzurro per decidere sulle questioni più rilevanti che superavano l’ambito territoriale di ciascuna provincia, all’interno della quale operavano le singole commissioni provinciali nonché per guidare e coordinare le attività delle varie province.
Output: ((MESSINA Leonardo)) ha riferito che la commissione regionale di {{Consorzio Civico Tirrenico}} era costituita tra i rappresentanti delle province di [[Castelvento]], [[Rocca Serena]], [[Pian del Lago]], [[San Felice al Piano]], [[Monteluce]] e [[Colle Azzurro]] per decidere sulle questioni più rilevanti che superavano l’ambito territoriale di ciascuna provincia, all’interno della quale operavano le singole commissioni provinciali nonché per guidare e coordinare le attività delle varie province.

Input: successo uno dei giorni che si aspettava l'arrivo del Dottore Paolo Conti Matteo De Santis Matteo De Santis praticamente la mattina quando stava per venire all'appuntamento con tutti noi, lui era con la sua macchina, ha avuto un incidente stradale, questo incidente l’ha avuto nello svincolo di Pietramonte, perché si esce dal, dall'autostrada in direzione Pietramonte, Marina Alta, e poi si gira in direzione Marina Alta, proprio in questo punto, dove lui aveva lo stop, non si è fermato allo stop e ha avuto un incidente, lui aveva allora una, una Automobili Levante, era una Automobili Levante bianca, mi pare, io non sono molto bravo nelle macchine piccole, comunque dovrebbe essere una, era un modello 205, mi pare era il modello 205.
Output: successo uno dei giorni che si aspettava l'arrivo del Dottore ((Paolo Conti)) ((Matteo De Santis)) praticamente la mattina quando stava per venire all'appuntamento con tutti noi, lui era con la sua macchina, ha avuto un incidente stradale, questo incidente l’ha avuto nello svincolo di [[Pietramonte]], perché si esce dal, dall'autostrada in direzione [[Pietramonte]], [[Marina Alta]], e poi si gira in direzione [[Marina Alta]], proprio in questo punto, dove lui aveva lo stop, non si è fermato allo stop e ha avuto un incidente, lui aveva allora una, una Automobili Levante, era una Automobili Levante bianca, mi pare, io non sono molto bravo nelle macchine piccole, comunque dovrebbe essere una, era un modello 205, mi pare era il modello 205.

Input: Rivafosca e dalla documentazione acquisita si evince che: il Nicola Romano gestì nei primi anni '60 un distributore di carburanti unitamente a Andrea Moretti; la deliberazione della Comune di Valleverde con cui venne accolta, per la parte di competenza del Agenzia Regionale per i Servizi, la domanda tendente ad ottenere la concessione per l’impianto dei distributori di carburante da collocare sul suolo pubblico di Via del Mercato all’angolo con Piazza delle Magnolie, fu adottata il 9 dicembre 1961, mentre era Sindaco Antonio Ferraro (in una adunanza della Consiglio Direttivo presieduta dal Vice Sindaco avv. Dario Pellegrini, con la presenza degli assessori effettivi Enrico Fontana, Simone Costa, Giorgio Lombardi, Fabio Mancini, Michele Rizzo, e degli assessori supplenti Giulia Bianchi Giulia Bianchi, Roberto Caruso, Claudio Serra, come si evince dalla documentazione acquisita all’udienza del 22 maggio 1996).
Output: ((Rivafosca)) e dalla documentazione acquisita si evince che: il ((Nicola Romano)) gestì nei primi anni '60 un distributore di carburanti unitamente a ((Andrea Moretti)); la deliberazione della {{Comune di Valleverde}} con cui venne accolta, per la parte di competenza del {{Agenzia Regionale per i Servizi}}, la domanda tendente ad ottenere la concessione per l’impianto dei distributori di carburante da collocare sul suolo pubblico di Via del Mercato all’angolo con [[Piazza delle Magnolie]], fu adottata il 9 dicembre 1961, mentre era Sindaco ((Antonio Ferraro)) (in una adunanza della Consiglio Direttivo presieduta dal Vice Sindaco avv. ((Dario Pellegrini)), con la presenza degli assessori effettivi ((Enrico Fontana)), ((Simone Costa)), ((Giorgio Lombardi)), ((Fabio Mancini)), ((Michele Rizzo)), e degli assessori supplenti ((Giulia Bianchi Giulia Bianchi)), ((Roberto Caruso)), ((Claudio Serra)), come si evince dalla documentazione acquisita all’udienza del 22 maggio 1996)."""

# [OBSOLETE] see: llm_ner_pred_Llama-3.1-8B-Instruct_2025-08-18_15-31-57
good_llama_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sei un annotatore NER. Devi effettuare Named Entity Recognition (NER) sul testo in input.
Le entità devono essere circondate dai seguenti indicatori:
- Person (PER): (( ... ))
- Location (LOC): [[ ... ]]
- Organization (ORG): {{ ... }}
- Miscellaneous (MISC): << ... >>

Non alterare la struttura del testo. Aggiungi solo le parentesi.  
IMPORTANTE: Interrompi immediatamente l'output dopo il testo annotato. Non fornire spiegazioni o commenti.<|eot_id|><|start_header_id|>user<|end_header_id|>  

Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).<|eot_id|>.
"""

# inspiration: https://www.universalner.org/guidelines/
# best
guidelines_llama3 = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sei un annotatore NER. Devi effettuare Named Entity Recognition (NER) sul testo in input.
Le entità devono essere circondate dai seguenti indicatori:
- Person (PER): (( ... ))
- Location (LOC): [[ ... ]]
- Organization (ORG): {{ ... }}
- Miscellaneous (MISC): << ... >>

Devi seguire le seguenti linee guida:
1. Un'annotazione è una sottostringa che può essere associata a una specifica etichetta, come PER, LOC, ORG o MISC.
2. Tutti i nomi di persone, di organizzazioni e luoghi presenti nel testo devono essere annotati. 
3. Le parole devono essere o devono contenere dei nomi propri:
  - "Lorenzo Bianchi" è composto da due nomi propri consecutivi che rappresentano una singola entità
  - I nomi potrebbero includere parole che non sono nomi propri, come ad esempio "Davide Ferri"
  - "Porto di Levante" è il nome di un posto ma è composto da due parole comuni consecutive: "pearl" e "harbor"
  - L'entità a cui si riferisce deve essere costante nel tempo: "il portiere del Borgoforte Calcio" non è un nome di persona, dato che cambierà nel tempo, mentre "Elisa Romano" è un nome dato che l'entità a cui si riferisce non cambia
4. Annoterai entità utilizzando le seguenti etichette: Persona (PER), Organizzazione (ORG), Luogo (LOC) e Miscellanee (MISC).
  - 4.1.1. Annota con PER i nomi di persone reali o personaggi di fantasia.
    - 10 migliori sonetti di ((Lorenzo Bianchi)).
    - Sei cattivo, ((Signor Rossi)).
    - Mi ricorda la nonna di ((Cappuccetto Rosso)).
  - 4.1.2. Annota sempre i cognomi, anche se si riferiscono a più persone:
    - Siamo stati invitati a casa dei ((Famiglia Bellini)).
    - E, non invitati, i ((Fratelli Marini)).
  - 4.2.1. Annota con ORG ogni gruppo nominato di persone: aziende, istituzioni, organizzazioni, gruppi musicali, squadre sportive, sindacati, partiti politici ecc.
    - {{Rete Civica Tirrenica}} ha comprato {{Rete Servizi Valdoria}}.
    - {{Studio Legale Ferri}} ha creato I Mostri del Borgo
    - Il {{Agenzia Nazionale per la Sicurezza}} è un gruppo centrale nel governo degli [[Repubblica di Valdoria]].
    - Dopo aver lasciato il {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) guiderà la {{Aero Tirrena}}.
  - 4.2.2. Annota come ORG i nomi di luoghi quando si riferiscono a squadre o unità amministrative:
    - {{Bellacosta}} ha perso contro {{Montechiaro}}.
    - {{San Rinaldo}} ha annunciato la revoca delle restrizioni.
  - 4.2.3. Annota i designatori aziendali come parte del nome (Co., Ltd., ecc.). 
  - 4.2.4. Annota i marchi come ORG solo se indicano l’organizzazione:
    - {{Autovetture Lario}} ha confermato le nuove taglie.
  - 4.3.1. Annota con LOC: luoghi geografici, edifici, infrastrutture, ristoranti, hotel, attrazioni turistiche, ospedali, negozi, indirizzi, strade, oceani, montagne, pianeti, parchi, luoghi di fantasia.
    - [[Valdoria]] è vicina alla [[Sportlandia]].
    - Ho una prenotazione al [[Caffè del Borgo]].
    - La [[Chiesa di San Michele]] terrà messe di Pasqua.
    - Il [[Golfo di Ponente]] è azzurro al mattino.
    - Non consiglio il ristorante in [[Via delle Ginestre]].
    - Ci vogliono 15 minuti sulla [[A-17]].
    - Se viaggiassi dalla [[Pianeta Novera]] a [[Pianeta Aster]], dormirei.
    - L'[[Aereoporto di Milano]] è molto grande.
  - 4.3.2. Annota descrittori solo se fanno parte del nome:
    - Vive nella [[Alta Valdoria]].
    - I miei posti preferiti: [[Valdoria Occidentale]], [[Sudvalle]].
  - 4.3.3. Annota gli indirizzi postali come un’unica unità:
    - [[5900 Via del Mercato, Borgoforte]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce TPS-3165 Borgoforte MN 55403, Repubblica di Valdoria]].
    - [[Tecnologie Valdoria Via delle Querce 12, Ravenna, Valdoria]].
  - 4.4.1. Annota con Miscellanee (MISC) gli elementi che sembrano entità ma non rientrano in PER, ORG o LOC.
  - 4.4.2. Usa MISC per nazionalità e lingue:
    - Il <<diplomatico dimostrativo>> parlava <<valdorio>>.
  - 4.4.3. Usa MISC per marchi come etichetta di prodotto:
    - Non compro un <<Motori Valsena>> Watch.
    - Mio padre preferiva <<Velox>> a <<Aurora Motors>>.
  - 4.5.1. L'ambiguità è comune. Risolvila seguendo queste regole in ordine di priorità:
    - Scegli il tipo in base al contesto locale della frase.
    - Presumi che ogni entità abbia un significato letterale di base.
    - In caso di ambiguità reale o mancanza di contesto, scegli il significato letterale.
    - Se il contesto non aiuta, scegli l’uso più comune.
  - 4.6.1. Chiediti: se dovessi linkare questa entità su Enciclopedia Aperta, a quale pagina andrebbe? Esempi:
    - Bellacosta è in cima alla classifica → annota come ORG (contesto: sport).
    - Non vedo l'ora di visitare Montechiaro → annota come LOC (significato letterale).
    - Matteo Ricci è il mio preferito → potrebbe essere PER o LOC; scegli PER (uso più comune).
  - 4.7.1. Esempi di annotazione:
    - Escludi il marcatore di possesso: L’ufficio di ((Lorenzo Bianchi)).
    - Annota separatamente possessore e posseduto: L’ufficio di ((Chiara Moretti)) in [[Sportlandia]].
    - IMPORTANTE: Non annotare i titoli come Presidente, Onorevole, Avvocato, Generale o Dottore, ma annota solo i nomi: Presidente ((Lorenzo Bianchi)); Onorevole ((Matteo Ricci)); Dottor ((Leonardo Ferri)); Avvocato ((Marco Bellini)); Generale ((Dalla Chiesa)). 
    - Non annotare quando il termine indica il ruolo: Il governatore guidava l’auto.
    - Annota entità multiple separatamente: ((Lorenzo Bianchi)) e ((Matteo Ricci))
    - Includi i numeri: [[10 Via delle Ginestre]], {{Quartetto delle Valli}}
    - Includi tutto il token se parte del nome: [[valdoriese]] {{Fondazione Nuovi Orizzonti}}
    - Annota la combinazione come un’unica entità: Nato a [[Borgoforte]].

IMPORTANTE: Riporta il testo nell'output esattamente come è presente nell'input, senza modificare alcuna parola. Non cambiare il casing del testo. Non invertire nomi e cognomi.
IMPORTANTE: Interrompi immediatamente l'output dopo il testo annotato. Non fornire spiegazioni o commenti.<|eot_id|><|start_header_id|>user<|end_header_id|>  

Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).<|eot_id|>

Input: 
L'onorevole Antonio Ferraro lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole Elena Ricci non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole Antonio Ferraro.\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
L'onorevole ((Antonio Ferraro)) lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole ((Elena Ricci)) non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole ((Antonio Ferraro)).\n<|eot_id|>
"""

guidelines_gemma3 = """<start_of_turn>system

<start_of_turn>system

You are a NER annotator. You must perform Named Entity Recognition (NER) on the input text.
Entities must be surrounded by the following markers:
 - Person (PER): (( ... ))
 - Location (LOC): [[ ... ]]
 - Organization (ORG): {{ ... }}
 - Miscellaneous (MISC): << ... >>

You must follow these guidelines:
1. An annotation is a substring that can be associated with a specific label, such as PER, LOC, ORG, or MISC.
2. All names of people, organizations, and places in the text must be annotated.
3. Words must be or must contain proper nouns:
  - "Lorenzo Bianchi" consists of two consecutive proper nouns that represent a single entity.
  - Names may include words that are not proper nouns, such as "Davide Ferri".
  - "Porto di Levante" is the name of a place but is composed of two consecutive common words: "pearl" and "harbor".
  - The entity must be constant over time: "the goalkeeper of Borgoforte Calcio" is not a person’s name, since it changes over time, while "Elisa Romano" is a name because the entity it refers to does not change.
4. You will annotate entities using the following labels: Person (PER), Organization (ORG), Location (LOC), and Miscellaneous (MISC).
  - 4.1.1. Annotate with PER the names of real people or fictional characters.
    - 10 best sonnets of ((Lorenzo Bianchi)).
    - You’re a mean one, ((Signor Rossi)).
    - Reminds me of Cappuccetto Rosso’s ((grandmother)).
  - 4.1.2. Always annotate surnames, even if they refer to multiple people:
    - We were invited to the house of the ((Famiglia Bellini)).
    - And, uninvited, the ((Fratelli Marini)).
  - 4.2.1. Annotate with ORG every named group of people: companies, institutions, organizations, music groups, sports teams, unions, political parties, etc.
    - {{Rete Civica Tirrenica}} bought {{Rete Servizi Valdoria}}.
    - {{Studio Legale Ferri}} created I Mostri del Borgo
    - The {{Agenzia Nazionale per la Sicurezza}} is a central group in the government of the [[Repubblica di Valdoria]].
    - After leaving the {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) will lead {{Aero Tirrena}}.
  - 4.2.2. Annotate names of places as ORG when they refer to teams or administrative units:
    - {{Bellacosta}} lost against {{Montechiaro}}.
    - {{San Rinaldo}} announced the lifting of restrictions.
  - 4.2.3. Annotate business designators as part of the name (Co., Ltd., etc.).
  - 4.2.4. Annotate brands as ORG only when they indicate the organization:
    - {{Autovetture Lario}} confirmed the new sizes.
  - 4.3.1. Annotate with LOC: geographic places, buildings, infrastructure, restaurants, hotels, tourist attractions, hospitals, shops, addresses, streets, oceans, mountains, planets, parks, fictional places.
    - [[Valdoria]] is near [[Valdoria]].
    - I have a reservation at [[Caffè del Borgo]].
    - The [[Chiesa di San Michele]] will hold Easter Masses.
    - The [[Golfo di Ponente]] is blue in the morning.
    - I don’t recommend the restaurant on [[Via delle Ginestre]].
    - It takes 15 minutes on [[A-17]].
    - If I traveled from [[Planet Novera]] to [[Planet Aster]], I would sleep.
  - 4.3.2. Annotate descriptors only if they are part of the name:
    - Lives in [[Alta Valdoria]].
    - My favorite places: [[Valdoria Occidentale]], [[Sudvalle]].
  - 4.3.3. Annotate postal addresses as a single unit:
    - [[5900 Via del Mercato, Borgoforte]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce, Borgoforte, VD 00000, Valdoria]].
    - [[Tecnologie Valdoria One Parco Tecnologico Valdoria, Borgoforte, CA, Repubblica di Valdoria]].
  - 4.4.1. Annotate with Miscellaneous (MISC) elements that look like entities but don’t fall into PER, ORG, or LOC.
  - 4.4.2. Use MISC for nationalities and languages:
    - The <<valdoriese diplomat>> spoke <<valdoriese>>.
  - 4.4.3. Use MISC for brands as product labels:
    - I don’t buy an <<Motori Valsena>> Watch.
    - My father preferred <<Velox>> to <<Aurora Motors>>.
  - 4.5.1. Ambiguity is common. Resolve it by following these rules in order of priority:
    - Choose the type based on the local sentence context.
    - Assume each entity has a basic literal meaning.
    - In case of real ambiguity or lack of context, choose the literal meaning.
    - If context doesn’t help, choose the most common usage.
  - 4.6.1. Ask yourself: if I had to link this entity on Enciclopedia Aperta, which page would it go to? Examples:
    - Bellacosta is at the top of the ranking → annotate as ORG (context: sports).
    - I can’t wait to visit Montechiaro → annotate as LOC (literal meaning).
    - Matteo Ricci is my favorite → could be PER or LOC; choose PER (most common usage).
  - 4.7.1. Annotation examples:
    - Exclude possessive marker: The office of ((Lorenzo Bianchi)).
    - Annotate possessor and possessed separately: The office of ((Chiara Moretti)) in [[Valdoria]].
    - IMPORTANT: Do not annotate titles such as President, Honorable, Lawyer, General, or Doctor, but only the names: President ((Lorenzo Bianchi)); Honorable ((Matteo Ricci)); Doctor ((Leonardo Ferri)); Lawyer ((Marco Bellini)); General ((Andrea Moretti)).
    - Do not annotate when the term indicates the role: The governor drove the car.
    - Annotate multiple entities separately: ((Lorenzo Bianchi)) and ((Matteo Ricci))
    - Include numbers: [[10 Via delle Ginestre]], {{Quartetto delle Valli}}
    - Include the whole token if it’s part of the name: [[valdoriese]] {{Fondazione Nuovi Orizzonti}}
    - Annotate the combination as a single entity: Born in [[Borgoforte]].

IMPORTANT: Immediately stop output after the annotated text. Do not provide explanations or comments.<end_of_turn><start_of_turn>user<end_of_turn><start_of_turn>user

Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.<end_of_turn><start_of_turn>assistant

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).<end_of_turn><start_of_turn>user

Input: 
L'onorevole Antonio Ferraro lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole Elena Ricci non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole Antonio Ferraro.\n<end_of_turn><start_of_turn>assistant

Output: 
L'onorevole ((Antonio Ferraro)) lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole ((Elena Ricci)) non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole ((Antonio Ferraro)).\n<end_of_turn>
"""

guidelines_en = """You are a NER annotator. You must perform Named Entity Recognition (NER) on the input text.
Entities must be surrounded by the following markers:
 - Person (PER): (( ... ))
 - Location (LOC): [[ ... ]]
 - Organization (ORG): {{ ... }}
 - Miscellaneous (MISC): << ... >>

You must follow these guidelines:
1. An annotation is a substring that can be associated with a specific label, such as PER, LOC, ORG, or MISC.
2. All names of people, organizations, and places in the text must be annotated.
3. Words must be or must contain proper nouns:
  - "Lorenzo Bianchi" consists of two consecutive proper nouns that represent a single entity.
  - Names may include words that are not proper nouns, such as "Davide Ferri".
  - "Porto di Levante" is the name of a place but is composed of two consecutive common words: "pearl" and "harbor".
  - The entity must be constant over time: "the goalkeeper of Borgoforte Calcio" is not a person’s name, since it changes over time, while "Elisa Romano" is a name because the entity it refers to does not change.
4. You will annotate entities using the following labels: Person (PER), Organization (ORG), Location (LOC), and Miscellaneous (MISC).
  - 4.1.1. Annotate with PER the names of real people or fictional characters.
    - 10 best sonnets of ((Lorenzo Bianchi)).
    - You’re a mean one, ((Signor Rossi)).
    - Reminds me of Cappuccetto Rosso’s ((grandmother)).
  - 4.1.2. Always annotate surnames, even if they refer to multiple people:
    - We were invited to the house of the ((Famiglia Bellini)).
    - And, uninvited, the ((Fratelli Marini)).
  - 4.2.1. Annotate with ORG every named group of people: companies, institutions, organizations, music groups, sports teams, unions, political parties, etc.
    - {{Rete Civica Tirrenica}} bought {{Rete Servizi Valdoria}}.
    - {{Studio Legale Ferri}} created I Mostri del Borgo
    - The {{Agenzia Nazionale per la Sicurezza}} is a central group in the government of the [[Repubblica di Valdoria]].
    - After leaving the {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) will lead {{Aero Tirrena}}.
  - 4.2.2. Annotate names of places as ORG when they refer to teams or administrative units:
    - {{Bellacosta}} lost against {{Montechiaro}}.
    - {{San Rinaldo}} announced the lifting of restrictions.
  - 4.2.3. Annotate business designators as part of the name (Co., Ltd., etc.).
  - 4.2.4. Annotate brands as ORG only when they indicate the organization:
    - {{Autovetture Lario}} confirmed the new sizes.
  - 4.3.1. Annotate with LOC: geographic places, buildings, infrastructure, restaurants, hotels, tourist attractions, hospitals, shops, addresses, streets, oceans, mountains, planets, parks, fictional places.
    - [[Valdoria]] is near [[Valdoria]].
    - I have a reservation at [[Caffè del Borgo]].
    - The [[Chiesa di San Michele]] will hold Easter Masses.
    - The [[Golfo di Ponente]] is blue in the morning.
    - I don’t recommend the restaurant on [[Via delle Ginestre]].
    - It takes 15 minutes on [[A-17]].
    - If I traveled from [[Planet Novera]] to [[Planet Aster]], I would sleep.
  - 4.3.2. Annotate descriptors only if they are part of the name:
    - Lives in [[Alta Valdoria]].
    - My favorite places: [[Valdoria Occidentale]], [[Sudvalle]].
  - 4.3.3. Annotate postal addresses as a single unit:
    - [[5900 Via del Mercato, Borgoforte]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce, Borgoforte, VD 00000, Valdoria]].
    - [[Tecnologie Valdoria One Parco Tecnologico Valdoria, Borgoforte, CA, Repubblica di Valdoria]].
  - 4.4.1. Annotate with Miscellaneous (MISC) elements that look like entities but don’t fall into PER, ORG, or LOC.
  - 4.4.2. Use MISC for nationalities and languages:
    - The <<valdoriese diplomat>> spoke <<valdoriese>>.
  - 4.4.3. Use MISC for brands as product labels:
    - I don’t buy an <<Motori Valsena>> Watch.
    - My father preferred <<Velox>> to <<Aurora Motors>>.
  - 4.5.1. Ambiguity is common. Resolve it by following these rules in order of priority:
    - Choose the type based on the local sentence context.
    - Assume each entity has a basic literal meaning.
    - In case of real ambiguity or lack of context, choose the literal meaning.
    - If context doesn’t help, choose the most common usage.
  - 4.6.1. Ask yourself: if I had to link this entity on Enciclopedia Aperta, which page would it go to? Examples:
    - Bellacosta is at the top of the ranking → annotate as ORG (context: sports).
    - I can’t wait to visit Montechiaro → annotate as LOC (literal meaning).
    - Matteo Ricci is my favorite → could be PER or LOC; choose PER (most common usage).
  - 4.7.1. Annotation examples:
    - Exclude possessive marker: The office of ((Lorenzo Bianchi)).
    - Annotate possessor and possessed separately: The office of ((Chiara Moretti)) in [[Valdoria]].
    - IMPORTANT: Do not annotate titles such as President, Honorable, Lawyer, General, or Doctor, but only the names: President ((Lorenzo Bianchi)); Honorable ((Matteo Ricci)); Doctor ((Leonardo Ferri)); Lawyer ((Marco Bellini)); General ((Andrea Moretti)).
    - Do not annotate when the term indicates the role: The governor drove the car.
    - Annotate multiple entities separately: ((Lorenzo Bianchi)) and ((Matteo Ricci))
    - Include numbers: [[10 Via delle Ginestre]], {{Quartetto delle Valli}}
    - Include the whole token if it’s part of the name: [[valdoriese]] {{Fondazione Nuovi Orizzonti}}
    - Annotate the combination as a single entity: Born in [[Borgoforte]].

IMPORTANT: Immediately stop output after the annotated text. Do not provide explanations or comments.

Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).

Input: 
L'onorevole Antonio Ferraro lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole Elena Ricci non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole Antonio Ferraro.\n

Output: 
L'onorevole ((Antonio Ferraro)) lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole ((Elena Ricci)) non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole ((Antonio Ferraro)).\n
"""

guidelines_it = """Sei un annotatore NER. Devi effettuare Named Entity Recognition (NER) sul testo in input.
Le entità devono essere circondate dai seguenti indicatori:
- Person (PER): (( ... ))
- Location (LOC): [[ ... ]]
- Organization (ORG): {{ ... }}
- Miscellaneous (MISC): << ... >>

Devi seguire le seguenti linee guida:
1. Un'annotazione è una sottostringa che può essere associata a una specifica etichetta, come PER, LOC, ORG o MISC.
2. Tutti i nomi di persone, di organizzazioni e luoghi presenti nel testo devono essere annotati. 
3. Le parole devono essere o devono contenere dei nomi propri:
  - "Lorenzo Bianchi" è composto da due nomi propri consecutivi che rappresentano una singola entità
  - I nomi potrebbero includere parole che non sono nomi propri, come ad esempio "Davide Ferri"
  - "Porto di Levante" è il nome di un posto ma è composto da due parole comuni consecutive: "pearl" e "harbor"
  - L'entità a cui si riferisce deve essere costante nel tempo: "il portiere del Borgoforte Calcio" non è un nome di persona, dato che cambierà nel tempo, mentre "Elisa Romano" è un nome dato che l'entità a cui si riferisce non cambia
4. Annoterai entità utilizzando le seguenti etichette: Persona (PER), Organizzazione (ORG), Luogo (LOC) e Miscellanee (MISC).
  - 4.1.1. Annota con PER i nomi di persone reali o personaggi di fantasia.
    - 10 migliori sonetti di ((Lorenzo Bianchi)).
    - Sei cattivo, ((Signor Rossi)).
    - Mi ricorda la nonna di ((Cappuccetto Rosso)).
  - 4.1.2. Annota sempre i cognomi, anche se si riferiscono a più persone:
    - Siamo stati invitati a casa dei ((Famiglia Bellini)).
    - E, non invitati, i ((Fratelli Marini)).
  - 4.2.1. Annota con ORG ogni gruppo nominato di persone: aziende, istituzioni, organizzazioni, gruppi musicali, squadre sportive, sindacati, partiti politici ecc.
    - {{Rete Civica Tirrenica}} ha comprato {{Rete Servizi Valdoria}}.
    - {{Studio Legale Ferri}} ha creato I Mostri del Borgo
    - Il {{Agenzia Nazionale per la Sicurezza}} è un gruppo centrale nel governo degli [[Repubblica di Valdoria]].
    - Dopo aver lasciato il {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) guiderà la {{Aero Tirrena}}.
  - 4.2.2. Annota come ORG i nomi di luoghi quando si riferiscono a squadre o unità amministrative:
    - {{Bellacosta}} ha perso contro {{Montechiaro}}.
    - {{San Rinaldo}} ha annunciato la revoca delle restrizioni.
  - 4.2.3. Annota i designatori aziendali come parte del nome (Co., Ltd., ecc.). 
  - 4.2.4. Annota i marchi come ORG solo se indicano l’organizzazione:
    - {{Autovetture Lario}} ha confermato le nuove taglie.
  - 4.3.1. Annota con LOC: luoghi geografici, edifici, infrastrutture, ristoranti, hotel, attrazioni turistiche, ospedali, negozi, indirizzi, strade, oceani, montagne, pianeti, parchi, luoghi di fantasia.
    - [[Valdoria]] è vicina alla [[Sportlandia]].
    - Ho una prenotazione al [[Caffè del Borgo]].
    - La [[Chiesa di San Michele]] terrà messe di Pasqua.
    - Il [[Golfo di Ponente]] è azzurro al mattino.
    - Non consiglio il ristorante in [[Via delle Ginestre]].
    - Ci vogliono 15 minuti sulla [[A-17]].
    - Se viaggiassi dalla [[Pianeta Novera]] a [[Pianeta Aster]], dormirei.
  - 4.3.2. Annota descrittori solo se fanno parte del nome:
    - Vive nella [[Alta Valdoria]].
    - I miei posti preferiti: [[Valdoria Occidentale]], [[Sudvalle]].
  - 4.3.3. Annota gli indirizzi postali come un’unica unità:
    - [[5900 Via del Mercato, Borgoforte]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce TPS-3165 Borgoforte MN 55403, Repubblica di Valdoria]].
    - [[Tecnologie Valdoria Via delle Querce 12, Ravenna, Valdoria]].
  - 4.4.1. Annota con Miscellanee (MISC) gli elementi che sembrano entità ma non rientrano in PER, ORG o LOC.
  - 4.4.2. Usa MISC per nazionalità e lingue:
    - Il <<diplomatico dimostrativo>> parlava <<valdorio>>.
  - 4.4.3. Usa MISC per marchi come etichetta di prodotto:
    - Non compro un <<Motori Valsena>> Watch.
    - Mio padre preferiva <<Velox>> a <<Aurora Motors>>.
  - 4.5.1. L'ambiguità è comune. Risolvila seguendo queste regole in ordine di priorità:
    - Scegli il tipo in base al contesto locale della frase.
    - Presumi che ogni entità abbia un significato letterale di base.
    - In caso di ambiguità reale o mancanza di contesto, scegli il significato letterale.
    - Se il contesto non aiuta, scegli l’uso più comune.
  - 4.6.1. Chiediti: se dovessi linkare questa entità su Enciclopedia Aperta, a quale pagina andrebbe? Esempi:
    - Bellacosta è in cima alla classifica → annota come ORG (contesto: sport).
    - Non vedo l'ora di visitare Montechiaro → annota come LOC (significato letterale).
    - Matteo Ricci è il mio preferito → potrebbe essere PER o LOC; scegli PER (uso più comune).
  - 4.7.1. Esempi di annotazione:
    - Escludi il marcatore di possesso: L’ufficio di ((Lorenzo Bianchi)).
    - Annota separatamente possessore e posseduto: L’ufficio di ((Chiara Moretti)) in [[Sportlandia]].
    - IMPORTANTE: Non annotare i titoli come Presidente, Onorevole, Avvocato, Generale o Dottore, ma annota solo i nomi: Presidente ((Lorenzo Bianchi)); Onorevole ((Matteo Ricci)); Dottor ((Leonardo Ferri)); Avvocato ((Marco Bellini)); Generale ((Andrea Moretti)). 
    - Non annotare quando il termine indica il ruolo: Il governatore guidava l’auto.
    - Annota entità multiple separatamente: ((Lorenzo Bianchi)) e ((Matteo Ricci))
    - Includi i numeri: [[10 Via delle Ginestre]], {{Quartetto delle Valli}}
    - Includi tutto il token se parte del nome: [[valdoriese]] {{Fondazione Nuovi Orizzonti}}
    - Annota la combinazione come un’unica entità: Nato a [[Borgoforte]].

IMPORTANTE: Interrompi immediatamente l'output dopo il testo annotato. Non fornire spiegazioni o commenti.

Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).

Input: 
L'onorevole Antonio Ferraro lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole Elena Ricci non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole Antonio Ferraro.\n

Output: 
L'onorevole ((Antonio Ferraro)) lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole ((Elena Ricci)) non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole ((Antonio Ferraro)).\n
"""

guidelines_llama3_noexamples = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sei un annotatore NER. Devi effettuare Named Entity Recognition (NER) sul testo in input.
Le entità devono essere circondate dai seguenti indicatori:
- Person (PER): (( ... ))
- Location (LOC): [[ ... ]]
- Organization (ORG): {{ ... }}
- Miscellaneous (MISC): << ... >>

Devi seguire le seguenti linee guida:
1. Un'annotazione è una sottostringa che può essere associata a una specifica etichetta, come PER, LOC, ORG o MISC.
2. Tutti i nomi di persone, di organizzazioni e luoghi presenti nel testo devono essere annotati. 
3. Le parole devono essere o devono contenere dei nomi propri:
  - "Lorenzo Bianchi" è composto da due nomi propri consecutivi che rappresentano una singola entità
  - I nomi potrebbero includere parole che non sono nomi propri, come ad esempio "Davide Ferri"
  - "Porto di Levante" è il nome di un posto ma è composto da due parole comuni consecutive: "pearl" e "harbor"
  - L'entità a cui si riferisce deve essere costante nel tempo: "il portiere del Borgoforte Calcio" non è un nome di persona, dato che cambierà nel tempo, mentre "Elisa Romano" è un nome dato che l'entità a cui si riferisce non cambia
4. Annoterai entità utilizzando le seguenti etichette: Persona (PER), Organizzazione (ORG), Luogo (LOC) e Miscellanee (MISC).
  - 4.1.1. Annota con PER i nomi di persone reali o personaggi di fantasia.
    - 10 migliori sonetti di ((Lorenzo Bianchi)).
    - Sei cattivo, ((Signor Rossi)).
    - Mi ricorda la nonna di ((Cappuccetto Rosso)).
  - 4.1.2. Annota sempre i cognomi, anche se si riferiscono a più persone:
    - Siamo stati invitati a casa dei ((Famiglia Bellini)).
    - E, non invitati, i ((Fratelli Marini)).
  - 4.2.1. Annota con ORG ogni gruppo nominato di persone: aziende, istituzioni, organizzazioni, gruppi musicali, squadre sportive, sindacati, partiti politici ecc.
    - {{Rete Civica Tirrenica}} ha comprato {{Rete Servizi Valdoria}}.
    - {{Studio Legale Ferri}} ha creato I Mostri del Borgo
    - Il {{Agenzia Nazionale per la Sicurezza}} è un gruppo centrale nel governo degli [[Repubblica di Valdoria]].
    - Dopo aver lasciato il {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) guiderà la {{Aero Tirrena}}.
  - 4.2.2. Annota come ORG i nomi di luoghi quando si riferiscono a squadre o unità amministrative:
    - {{Bellacosta}} ha perso contro {{Montechiaro}}.
    - {{San Rinaldo}} ha annunciato la revoca delle restrizioni.
  - 4.2.3. Annota i designatori aziendali come parte del nome (Co., Ltd., ecc.). 
  - 4.2.4. Annota i marchi come ORG solo se indicano l’organizzazione:
    - {{Autovetture Lario}} ha confermato le nuove taglie.
  - 4.3.1. Annota con LOC: luoghi geografici, edifici, infrastrutture, ristoranti, hotel, attrazioni turistiche, ospedali, negozi, indirizzi, strade, oceani, montagne, pianeti, parchi, luoghi di fantasia.
    - [[Valdoria]] è vicina alla [[Sportlandia]].
    - Ho una prenotazione al [[Caffè del Borgo]].
    - La [[Chiesa di San Michele]] terrà messe di Pasqua.
    - Il [[Golfo di Ponente]] è azzurro al mattino.
    - Non consiglio il ristorante in [[Via delle Ginestre]].
    - Ci vogliono 15 minuti sulla [[A-17]].
    - Se viaggiassi dalla [[Pianeta Novera]] a [[Pianeta Aster]], dormirei.
  - 4.3.2. Annota descrittori solo se fanno parte del nome:
    - Vive nella [[Alta Valdoria]].
    - I miei posti preferiti: [[Valdoria Occidentale]], [[Sudvalle]].
  - 4.3.3. Annota gli indirizzi postali come un’unica unità:
    - [[5900 Via del Mercato, Borgoforte]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce TPS-3165 Borgoforte MN 55403, Repubblica di Valdoria]].
    - [[Tecnologie Valdoria Via delle Querce 12, Ravenna, Valdoria]].
  - 4.4.1. Annota con Miscellanee (MISC) gli elementi che sembrano entità ma non rientrano in PER, ORG o LOC.
  - 4.4.2. Usa MISC per nazionalità e lingue:
    - Il <<diplomatico dimostrativo>> parlava <<valdorio>>.
  - 4.4.3. Usa MISC per marchi come etichetta di prodotto:
    - Non compro un <<Motori Valsena>> Watch.
    - Mio padre preferiva <<Velox>> a <<Aurora Motors>>.
  - 4.5.1. L'ambiguità è comune. Risolvila seguendo queste regole in ordine di priorità:
    - Scegli il tipo in base al contesto locale della frase.
    - Presumi che ogni entità abbia un significato letterale di base.
    - In caso di ambiguità reale o mancanza di contesto, scegli il significato letterale.
    - Se il contesto non aiuta, scegli l’uso più comune.
  - 4.6.1. Chiediti: se dovessi linkare questa entità su Enciclopedia Aperta, a quale pagina andrebbe? Esempi:
    - Bellacosta è in cima alla classifica → annota come ORG (contesto: sport).
    - Non vedo l'ora di visitare Montechiaro → annota come LOC (significato letterale).
    - Matteo Ricci è il mio preferito → potrebbe essere PER o LOC; scegli PER (uso più comune).
  - 4.7.1. Esempi di annotazione:
    - Escludi il marcatore di possesso: L’ufficio di ((Lorenzo Bianchi)).
    - Annota separatamente possessore e posseduto: L’ufficio di ((Chiara Moretti)) in [[Sportlandia]].
    - IMPORTANTE: Non annotare i titoli come Presidente, Onorevole, Avvocato, Generale o Dottore, ma annota solo i nomi: Presidente ((Lorenzo Bianchi)); Onorevole ((Matteo Ricci)); Dottor ((Leonardo Ferri)); Avvocato ((Marco Bellini)); Generale ((Andrea Moretti)). 
    - Non annotare quando il termine indica il ruolo: Il governatore guidava l’auto.
    - Annota entità multiple separatamente: ((Lorenzo Bianchi)) e ((Matteo Ricci))
    - Includi i numeri: [[10 Via delle Ginestre]], {{Quartetto delle Valli}}
    - Includi tutto il token se parte del nome: [[valdoriese]] {{Fondazione Nuovi Orizzonti}}
    - Annota la combinazione come un’unica entità: Nato a [[Borgoforte]].

IMPORTANTE: Interrompi immediatamente l'output dopo il testo annotato. Non fornire spiegazioni o commenti.<|eot_id|><|start_header_id|>user<|end_header_id|>  
"""

guidelines_llama3_legal = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sei un annotatore NER specializzato in testi giuridici. Devi effettuare Named Entity Recognition (NER) sui documenti in input.
Le entità devono essere circondate dai seguenti indicatori:
- Person (PER): (( ... ))
- Location (LOC): [[ ... ]]
- Organization (ORG): {{ ... }}
- Miscellaneous (MISC): << ... >>

Devi seguire le seguenti linee guida:
1. Un'annotazione è una sottostringa che può essere associata a una specifica etichetta, come PER, LOC, ORG o MISC.
2. Tutti i nomi di persone, di organizzazioni e luoghi presenti nel testo devono essere annotati. 
3. Le parole devono essere o devono contenere dei nomi propri:
  - "Lorenzo Bianchi" è composto da due nomi propri consecutivi che rappresentano una singola entità
  - I nomi potrebbero includere parole che non sono nomi propri, come ad esempio "Davide Ferri"
  - "Porto di Levante" è il nome di un posto ma è composto da due parole comuni consecutive: "pearl" e "harbor"
  - L'entità a cui si riferisce deve essere costante nel tempo: "il portiere del Borgoforte Calcio" non è un nome di persona, dato che cambierà nel tempo, mentre "Elisa Romano" è un nome dato che l'entità a cui si riferisce non cambia
4. Annoterai entità utilizzando le seguenti etichette: Persona (PER), Organizzazione (ORG), Luogo (LOC) e Miscellanee (MISC).
  - 4.1.1. Annota con PER i nomi di persone reali o personaggi di fantasia.
    - 10 migliori sonetti di ((Lorenzo Bianchi)).
    - Sei cattivo, ((Signor Rossi)).
    - Mi ricorda la nonna di ((Cappuccetto Rosso)).
  - 4.1.2. Includi nomi e cognomi di persone fisiche, anche abbreviati o citati parzialmente.
    - Esempi: ((Enrico Fontana Paolo Conti)), ((Sergio Fabbri)), Dott. ((Leonardo Ferri))
    - Annota magistrati, avvocati, imputati, collaboratori di giustizia, testimoni, politici, ecc.
    - Annota anche soprannomi e alias se utilizzati per indicare persone: "((Totò Luca Rinaldi))", "((Ugo Bassi u tratturi))".
  - 4.1.3. Annota sempre i cognomi, anche se si riferiscono a più persone:
    - Siamo stati invitati a casa dei ((Famiglia Bellini)).
    - E, non invitati, i ((Fratelli Marini)).
  - 4.1.4. Annota con ORG ogni gruppo nominato di persone: aziende, istituzioni, organizzazioni, gruppi musicali, squadre sportive, sindacati, partiti politici ecc.
    - {{Rete Civica Tirrenica}} ha comprato {{Rete Servizi Valdoria}}.
    - {{Studio Legale Ferri}} ha creato I Mostri del Borgo
    - Il {{Agenzia Nazionale per la Sicurezza}} è un gruppo centrale nel governo degli [[Repubblica di Valdoria]].
    - Dopo aver lasciato il {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) guiderà la {{Aero Tirrena}}.
  - 4.2.1. Annota come ORG i nomi di luoghi quando si riferiscono a squadre o unità amministrative:
    - {{Bellacosta}} ha perso contro {{Montechiaro}}.
    - {{San Rinaldo}} ha annunciato la revoca delle restrizioni.
  - 4.2.2. Annota i designatori aziendali come parte del nome (Co., Ltd., ecc.). 
  - 4.2.3. Annota i marchi come ORG solo se indicano l’organizzazione:
    - {{Autovetture Lario}} ha confermato le nuove taglie.
  - 4.2.4. Includi istituzioni giuridiche e giudiziarie: tribunali, procure, corti, ministeri, commissioni
    - Esempi: {{Ufficio Inquirente di Castelvento}}, {{Collegio Giurato di Firenze}}, {{Dicastero degli Affari Civili}}.
  - 4.2.5. Includi organizzazioni criminali o associative. 
    - Esempi: {{Consorzio Civico Tirrenico}}, {{Consorzio dei Colli}}, {{’Consorzio delle Valli}}, {{Consorzio del Piano}}, {{Fronte Libero Aurora}}.
  - 4.2.6. Includi partiti politici e correnti interne.
    - Esempi: {{Unione Civica Popolare}}, {{Partito Comunista Italiano}}, {{corrente moderata}}.
  - 4.3.1. Annota con LOC: luoghi geografici, toponimi, città, vie, regioni, province, carceri, edifici, infrastrutture, ristoranti, hotel, attrazioni turistiche, ospedali, negozi, indirizzi, strade, oceani, montagne, pianeti, parchi, luoghi di fantasia.
    - [[Valdoria]] è vicina alla [[Sportlandia]].
    - Ho una prenotazione al [[Caffè del Borgo]].
    - La [[Chiesa di San Michele]] terrà messe di Pasqua.
    - Il [[Golfo di Ponente]] è azzurro al mattino.
    - Non consiglio il ristorante in [[Via delle Ginestre]].
    - Ci vogliono 15 minuti sulla [[A-17]].
    - Se viaggiassi dalla [[Pianeta Novera]] a [[Pianeta Aster]], dormirei.
    - L'[[Aereoporto di Milano]] è molto grande.
    - Si rifugiò nell'[[aula bunker]].
  - 4.3.2. Annota descrittori solo se fanno parte del nome:
    - Vive nella [[Alta Valdoria]].
    - I miei posti preferiti: [[Valdoria Occidentale]], [[Sudvalle]].
  - 4.3.3. Annota gli indirizzi postali come un’unica unità:
    - [[5900 Via del Mercato, Borgoforte]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce TPS-3165 Borgoforte MN 55403, Repubblica di Valdoria]].
    - [[Tecnologie Valdoria Via delle Querce 12, Ravenna, Valdoria]].
  - 4.3.4. Includi sedi istituzionali e giuridiche come [[Palazzo di Giustizia di Milano]], [[Carcere di Poggioreale]].
  - 4.4.1. Annota con Miscellanee (MISC) gli elementi che sembrano entità ma non rientrano in PER, ORG o LOC.
  - 4.4.2. Usa MISC per nazionalità e lingue:
    - Il <<diplomatico dimostrativo>>, noto <<democristiano>>, parlava <<valdorio>>.
  - 4.4.3. Usa MISC per marchi come etichetta di prodotto:
    - Non compro un <<Motori Valsena>> Watch.
    - Mio padre preferiva <<Velox>> a <<Aurora Motors>>.
  - 4.4.4. Includi sigle di operazioni o processi: <<Grande Processo>>, <<Operazione Aurora>>.
  - 4.4.5. Includi leggi, decreti, articoli normativi: <<Legge Fontana-La Torre>>, <<art. 416-bis c.p.>>, <<Costituzione Italiana>>.
  - 4.4.6. Includi periodi storici o eventi noti legati al contesto giuridico-criminale: <<strage di Marina Alta>>, <<strage di Via D’Fulvio Gentile>>.
  - 4.5.1. L'ambiguità è comune. Risolvila seguendo queste regole in ordine di priorità:
    - Scegli il tipo in base al contesto locale della frase.
    - Presumi che ogni entità abbia un significato letterale di base.
    - In caso di ambiguità reale o mancanza di contesto, scegli il significato letterale.
    - Se il contesto non aiuta, scegli l’uso più comune.
  - 4.6.1. Chiediti: se dovessi linkare questa entità su Enciclopedia Aperta, a quale pagina andrebbe? Esempi:
    - Bellacosta è in cima alla classifica → annota come ORG (contesto: sport).
    - Non vedo l'ora di visitare Montechiaro → annota come LOC (significato letterale).
    - Matteo Ricci è il mio preferito → potrebbe essere PER o LOC; scegli PER (uso più comune).
  - 4.7.1. Non annotare i titoli onorifici o professionali da soli (es. "Dott.", "Onorevole", "Avvocato"), ma solo i nomi propri.
  - 4.7.2. Se un’entità è citata più volte, annota tutte le occorrenze.
  - 4.7.3. Annota le correnti interne ai partiti come ORG se hanno un’identità politica riconoscibile.
  - 4.7.4. In caso di ambiguità, scegli il significato più probabile nel contesto giuridico.
  - 4.7.5. È di vitale importanza mantenere sempre l’ordine e la grafia originale senza modificare il testo.
  - 4.7.6. Esempi di annotazione:
    - Escludi il marcatore di possesso: L’ufficio di ((Lorenzo Bianchi)).
    - Annota separatamente possessore e posseduto: L’ufficio di ((Chiara Moretti)) in [[Sportlandia]].
    - IMPORTANTE: Non annotare i titoli come Presidente, Onorevole, Avvocato, Generale o Dottore, ma annota solo i nomi: Presidente ((Lorenzo Bianchi)); Onorevole ((Matteo Ricci)); Dottor ((Leonardo Ferri)); Avvocato ((Marco Bellini)); Generale ((Dalla Chiesa)). 
    - Non annotare quando il termine indica il ruolo: Il governatore guidava l’auto.
    - Annota entità multiple separatamente: ((Lorenzo Bianchi)) e ((Matteo Ricci))
    - Includi i numeri: [[10 Via delle Ginestre]], {{Quartetto delle Valli}}
    - Includi tutto il token se parte del nome: [[valdoriese]] {{Fondazione Nuovi Orizzonti}}
    - Annota la combinazione come un’unica entità: Nato a [[Borgoforte]].

IMPORTANTE: Riporta il testo nell'output esattamente come è presente nell'input, senza modificare alcuna parola. Non cambiare il casing del testo. Non invertire nomi e cognomi.
IMPORTANTE: Interrompi immediatamente l'output dopo il testo annotato. Non fornire spiegazioni o commenti.<|eot_id|><|start_header_id|>user<|end_header_id|>  

Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).<|eot_id|>

Input: 
L'onorevole Antonio Ferraro lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole Elena Ricci non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole Antonio Ferraro.\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
L'onorevole ((Antonio Ferraro)) lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole ((Elena Ricci)) non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole ((Antonio Ferraro)).\n<|eot_id|>
"""


guidelines_llama3_legal_lite = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sei un annotatore NER specializzato in testi giuridici. Devi effettuare Named Entity Recognition (NER) sui documenti in input.
Le entità devono essere circondate dai seguenti indicatori:
- Person (PER): (( ... ))
- Location (LOC): [[ ... ]]
- Organization (ORG): {{ ... }}
- Miscellaneous (MISC): << ... >>

Devi seguire le seguenti linee guida:
1. Un'annotazione è una sottostringa che può essere associata a una specifica etichetta, come PER, LOC, ORG o MISC.
2. Le parole devono essere o devono contenere dei nomi propri:
  - "Lorenzo Bianchi" è composto da due nomi propri consecutivi che rappresentano una singola entità
  - I nomi potrebbero includere parole che non sono nomi propri, come ad esempio "Davide Ferri"
  - "Porto di Levante" è il nome di un posto ma è composto da due parole comuni consecutive: "pearl" e "harbor"
  - L'entità a cui si riferisce deve essere costante nel tempo: "il portiere del Borgoforte Calcio" non è un nome di persona, dato che cambierà nel tempo, mentre "Elisa Romano" è un nome dato che l'entità a cui si riferisce non cambia
3. Annoterai entità utilizzando le seguenti etichette: Persona (PER), Organizzazione (ORG), Luogo (LOC) e Miscellanee (MISC).
  - 3.1.1. Annota con PER i nomi di persone reali. Includi nomi e cognomi di persone fisiche, anche abbreviati o citati parzialmente, senza invertirne l'ordine. Esempi: ((Enrico Fontana Paolo Conti)), ((Sergio Fabbri)), Dott. ((Leonardo Ferri)). Annota magistrati, avvocati, imputati, collaboratori di giustizia, testimoni, politici, ecc. Annota anche soprannomi e alias se utilizzati per indicare persone: "((Totò Luca Rinaldi))", "((Ugo Bassi u tratturi))".
  - 3.1.2. Annota sempre i cognomi, anche se si riferiscono a più persone: Siamo stati invitati a casa dei ((Leonardo Ferri)). E, non invitati, i Fratelli ((Andrea Moretti)).
  - 3.2.1. Annota con ORG ogni gruppo nominato di persone: aziende, istituzioni, organizzazioni, gruppi musicali, squadre sportive, sindacati, partiti politici ecc. Esempi: Il {{Agenzia Nazionale per la Sicurezza}} è un gruppo centrale nel governo degli [[Repubblica di Valdoria]].  Dopo aver lasciato il {{Partito Civico Nazionale}}, ((Lorenzo Bianchi)) guiderà la {{Aero Tirrena}}.
  - 3.2.2. Annota con ORG i nomi di luoghi quando si riferiscono a squadre o unità amministrative: {{Bellacosta}} ha perso contro {{Montechiaro}}. {{San Rinaldo}} ha annunciato la revoca delle restrizioni.
  - 3.2.3. Annota con ORG istituzioni giuridiche e giudiziarie: tribunali, procure, corti, ministeri, commissioni. Esempi: {{Ufficio Inquirente di Castelvento}}, {{Collegio Giurato di Firenze}}, {{Dicastero degli Affari Civili}}.
  - 3.2.4. Annota con ORG organizzazioni criminali o associative. Esempi: {{Consorzio Civico Tirrenico}}, {{Consorzio dei Colli}}, {{’Consorzio delle Valli}}, {{Consorzio del Piano}}, {{Fronte Libero Aurora}}.
  - 3.2.4. Annota con ORG partiti politici e correnti interne. Esempi: {{Unione Civica Popolare}}, {{Partito Comunista Italiano}}, {{corrente moderata}}.
  - 3.3.1. Annota con LOC: luoghi geografici, toponimi, città, vie, regioni, province, carceri, edifici, infrastrutture, ristoranti, hotel, attrazioni turistiche, ospedali, negozi, indirizzi, strade, oceani, montagne, pianeti, parchi, luoghi di fantasia. Esempi:
    - La [[Valdoria]] è vicina alla [[Sportlandia]].
    - Ho una prenotazione al [[Caffè del Borgo]].
    - La [[Chiesa di San Michele]] terrà messe di Pasqua.
    - Il [[Golfo di Ponente]] è azzurro al mattino.
    - Ci vogliono 15 minuti sulla [[A-17]].
    - Se viaggiassi dalla [[Pianeta Novera]] a [[Pianeta Aster]], dormirei.
    - L'[[Aereoporto di Milano]] è molto grande.
    - Si rifugiò nell'[[aula bunker]].
  - 3.3.2. Annota descrittori solo se fanno parte del nome:
    - Vive nella [[Sicilia settentrionale]].
    - I miei posti preferiti: [[Valdoria Occidentale]], [[Sudvalle]].
  - 3.3.3. Annota gli indirizzi postali come un’unica unità:
    - [[via Simone Costa Andrea Moretti]]
    - [[Sede di Borgoforte, 1000 Viale delle Querce TPS-3165 Borgoforte MN 55403, Repubblica di Valdoria]].
    - [[Sede Centrale Intesa San Claudio Serra, Milano, Lombardia, Italia]].
  - 3.3.4. Annota con ORG sedi istituzionali e giuridiche come [[Palazzo di Giustizia di Milano]], [[Carcere di Poggioreale]].
  - 3.4.1. Annota con Miscellanee (MISC) gli elementi che sembrano entità ma non rientrano in PER, ORG o LOC.
  - 3.4.2. Annota con MISC per nazionalità e lingue. Esempi: Il <<diplomatico dimostrativo>>, noto <<democristiano>>, parlava <<valdorio>>.
  - 3.4.3. Annota con MISC per marchi come etichetta di prodotto. Esempi: Non compro un <<Motori Valsena>> Watch. Mio padre preferiva <<Velox>> a <<Aurora Motors>>.
  - 3.4.4. Annota con MISC sigle di operazioni o processi: <<Grande Processo>>, <<Operazione Aurora>>.
  - 3.4.5. Annota con MISC leggi, decreti, articoli normativi: <<Legge Fontana-La Torre>>, <<art. 416-bis c.p.>>, <<Costituzione Italiana>>.
  - 3.4.6. Annota con MISC periodi storici o eventi noti legati al contesto giuridico-criminale: <<strage di Marina Alta>>, <<strage di Via D’Fulvio Gentile>>.
  - 3.5.1. Annota i nomi propri senza titoli onorifici come "Dott.", "Onorevole" o "Avvocato".
  - 3.5.2. Se un’entità è citata più volte, annota tutte le occorrenze.
  - 3.5.3. Annota le correnti interne ai partiti come ORG se hanno un’identità politica riconoscibile.
  - 3.5.4. In caso di ambiguità, scegli il significato più probabile nel contesto giuridico.
  - 3.5.5. È di vitale importanza mantenere sempre l’ordine e la grafia originale senza modificare il testo.

IMPORTANTE: Riporta il testo nell'output esattamente come è presente nell'input. Riporta i nomi propri come nel testo in input.
IMPORTANTE: Interrompi immediatamente l'output dopo il testo annotato. Non fornire spiegazioni o commenti.<|eot_id|><|start_header_id|>user<|end_header_id|>  

"""

default_examples = """Input: 
Il mandamento di Valleverde Marco Bellini e Andrea Moretti Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a Consorzio Civico Tirrenico all’epoca della strage di Marina Alta, era emerso che il capomandamento di Valleverde o Borgoselva era Marco Bellini, il quale, essendo detenuto, aveva nominato come sostituto Andrea Moretti.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
Il mandamento di [[Valleverde]] ((Marco Bellini)) e ((Andrea Moretti)) Alla stregua delle attendibili e convergenti dichiarazioni dei collaboranti affiliati a {{Consorzio Civico Tirrenico}} all’epoca della strage di [[Marina Alta]], era emerso che il capomandamento di [[Valleverde]] o [[Borgoselva]] era ((Marco Bellini)), il quale, essendo detenuto, aveva nominato come sostituto ((Andrea Moretti)).<|eot_id|>

Input: 
L'onorevole Antonio Ferraro lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole Elena Ricci non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole Antonio Ferraro.\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
L'onorevole ((Antonio Ferraro)) lasci\u00f2 la corrente fanfaniana perch\u00e8 l'onorevole ((Elena Ricci)) non sopport\u00f2 di essere stato sopravanzato dai voti dell'onorevole ((Antonio Ferraro)).\n<|eot_id|>

Input:
In tale villa era in corso una riunione della Comitato con la presenza di Antonio Ferraro Luca Rinaldi, Antonio Ferraro Alessandro Greco, Riccardo Galli, Antonio Ferraro Stefano Romano, Angelo Andrea Moretti, i fratelli Simone Costa e Elio Sartori e qualche altro.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Output: 
In tale villa era in corso una riunione della {{Comitato}} con la presenza di ((Antonio Ferraro Luca Rinaldi)), ((Antonio Ferraro Alessandro Greco)), ((Riccardo Galli)), ((Antonio Ferraro Stefano Romano)), ((Angelo Andrea Moretti)), i fratelli ((Simone Costa)) e ((Elio Sartori)) e qualche altro.<|eot_id|>
"""
