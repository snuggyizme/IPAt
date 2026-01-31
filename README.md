# IPAt

IPAt is a GUI tool for batch-generating IPA transcriptions of wordlists using custom rulesets.

## Installation

This project uses **FreeSimpleGUI** and **Pyperclip**

Install all dependencies with:

    pip install -r requirements.txt

## Usage

### 1. Creating a Language
To get started with IPAt, you need to have a language config. If you have a conlang, head to *'Import/Create a language config'* and click *'Make new'*. If you want to try out IPAt without a conlang, skip to **2. Selecting a Language**.

![Alt: The navigation path from the homepage to the 'Make New' menu](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/1.png)

![](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/2.png)

Fill in the name of your language and the highest grapheme length that can exist in your language (e.g. English is 4: "ough", "eigh", "aigh"):


![Alt: The 'Make New' menu with 'Example Language' in the 'Name' field and 3 in the 'Longest Graph' field](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/3.png)

Click *'Save and Continue'*. You can now begin adding grapheme-phoneme pairs to your language. After adding each sound, click *'Add sound'*. When you are finished, click *'Finish'*.

![Alt: The 'Add Sounds' menu with the grapheme 'A' and the phoneme 'æ'](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/4.png)

![Alt: The 'Add Sounds' menu with the grapheme 'Th' and the phoneme 'θ'](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/5.png)

### 2. Selecting a Language
Return to the homepage and select *'Create IPA for words'*, and then *'Select Language'*. Select the language you wish to use in IPAt. English will always be avaliable.

![Alt: The navigation path from the hoempage to the 'Select Language' menu](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/6.png)

![](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/7.png)

![Alt: The 'Select Language' menu showing two languages: English and 'Example Language'](https://raw.githubusercontent.com/snuggyizme/IPAt/main/img/8.png)
