## **Analyse comparative des IA**

### Table des matières

1. [Définition de la méthodologie](#définition-de-la-méthodologie)
2. [Configurations testées](#configurations-testées)
3. [Méthodologie des tests](#méthodologie-des-tests)
4. [Conclusions attendues](#conclusions-attendues)
5. [Résultats des tests](#résultats-des-tests)
   - [Gamma = 0.9, Alpha = 0.3 (IA1)](#gamma--09-alpha--03-ia1)
   - [Gamma = 0.3, Alpha = 0.3 (IA2)](#gamma--03-alpha--03-ia2)
   - [Gamma = 0.9, Alpha = 0.9 (IA3)](#gamma--09-alpha--09-ia3)
   - [Gamma = 0.9, Alpha = 0.1 (IA4)](#gamma--09-alpha--01-ia4)
6. [Conclusion](#conclusion)

---
### **Définition de la méthodologie**

Avant de procéder aux tests, il est essentiel de définir une méthodologie rigoureuse pour garantir des résultats pertinents. L'objectif est d'évaluer l'impact des hyperparamètres **Gamma** (facteur d'actualisation) et **Alpha** (facteur d'apprentissage) sur les performances des IA. Cette analyse se base sur trois configurations différentes de ces hyperparamètres, chacune visant à explorer des comportements d'apprentissage distincts.

---
### **Configurations testées**

Trois configurations de Gamma (facteur d'actualisation) et Alpha (facteur d'apprentissage) ont été définies. 
Chaque configuration est pensée pour représenter une stratégie d'apprentissage distincte, mettant en lumière les compromis entre récompenses immédiates et futures, ainsi que la vitesse d'intégration des nouvelles informations. Cette approche aide à mieux comprendre comment optimiser ces paramètres en fonction des objectifs du système.

1. **Gamma = 0.9, Alpha = 0.3**
2. **Gamma = 0.3, Alpha = 0.3**
3. **Gamma = 0.9, Alpha = 0.9**
4. **Gamma = 0.9, Alpha = 0.1**

---
### **Méthodologie des tests**

Pour chaque configuration, un test sera exécutée afin d'évaluer les performances des IA dans un environnement standardisé. Les étapes suivantes seront respectées :  
1. **Définir des métriques d'évaluation** : le taux de victoire contre une IA random.
2. **Exécuter un nombre suffisant de parties** : nous avons choisis d'entrainer nos IA sur 200 000 parties par palier de 50 000
3. **Evlotution du epsilon**: nous avons choisit de diminuer de 1% toutes les 500 parties
4. **Test des IA** : nous avons choisis d'évaluer les IA sur 5000 parties en joueur 1 et 5000 parties en joueur 2 toutes les 50 000 parties

---
### **Conclusions attendues**

En analysant les résultats obtenus, il sera possible de :
- Identifier la configuration la plus adaptée au jeu étudié.
- Comprendre l’impact de chaque hyperparamètre sur les performances de l’IA.
- Adapter les choix d’hyperparamètres pour optimiser l’apprentissage en fonction des objectifs du jeu.

Les conclusions détaillées seront fournies après l’exécution des tests et l’analyse des résultats.

---
### **Résultats des tests**
#### **Gamma = 0.9, Alpha = 0.3** (IA1)

##### 50 000
###### IA commence**
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 831             | 4169           |
| Games lost      | 4169            | 831            |
| Win percentage  | 16.62%          | 83.38%         |
| Lose percentage | 83.38%          | 16.62%         |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1495            | 3505           |
| Games lost      | 3505            | 1495           |
| Win percentage  | 29.90%          | 70.10%         |
| Lose percentage | 70.10%          | 29.90%         |

**BEST AI : AI**

##### 100 000
###### IA commence
| Metric          | RANDOM       | AI          |
|-----------------|--------------|-------------|
| Games won       | 984          | 4016        |
| Games lost      | 4016         | 984         |
| Win percentage  | 19.68%       | 80.32%      |
| Lose percentage | 80.32%       | 19.68%      |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM       | AI          |
|-----------------|--------------|-------------|
| Games won       | 1810         | 3190        |
| Games lost      | 3190         | 1810        |
| Win percentage  | 36.20%       | 63.80%      |
| Lose percentage | 63.80%       | 36.20%      |

**BEST AI : AI**

##### 150 000
*(Données manquantes)*

##### 200 000
*(Données manquantes)*

---
#### **Gamma = 0.3, Alpha = 0.3** (IA2)

##### 50 000
###### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1885            | 3115           |
| Games lost      | 3115            | 1885           |
| Win percentage  | 37.70%          | 62.30%         |
| Lose percentage | 62.30%          | 37.70%         |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 2187            | 2813           |
| Games lost      | 2813            | 2187           |
| Win percentage  | 43.74%          | 56.26%         |
| Lose percentage | 56.26%          | 43.74%         |

**BEST AI : AI**

##### 100 000
###### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1691            | 3309           |
| Games lost      | 3309            | 1691           |
| Win percentage  | 33.82%          | 66.18%         |
| Lose percentage | 66.18%          | 33.82%         |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 2112            | 2888           |
| Games lost      | 2888            | 2112           |
| Win percentage  | 42.24%          | 57.76%         |
| Lose percentage | 57.76%          | 42.24%         |

**BEST AI : AI**

##### 150 000
###### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1446            | 3554           |
| Games lost      | 3554            | 1446           |
| Win percentage  | 28.92%          | 71.08%         |
| Lose percentage | 71.08%          | 28.92%         |

**BEST AI : AI**
###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 2043            | 2957           |
| Games lost      | 2957            | 2043           |
| Win percentage  | 40.86%          | 59.14%         |
| Lose percentage | 59.14%          | 40.86%         |

**BEST AI : AI**

##### 200 000
###### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1719            | 3281           |
| Games lost      | 3281            | 1719           |
| Win percentage  | 34.38%          | 65.62%         |
| Lose percentage | 65.62%          | 34.38%         |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 2070            | 2930           |
| Games lost      | 2930            | 2070           |
| Win percentage  | 41.40%          | 58.60%         |
| Lose percentage | 58.60%          | 41.40%         |

##### Analyse globale des résultats 

![image](https://github.com/user-attachments/assets/a453495f-4666-40de-a55b-4fa0790e6dd7)

###### **IA commence :**
- À mesure que le nombre de parties augmente (jusqu'à 150 000), les performances augmentent, suggérant que l'IA apprend efficacement les meilleures actions dans l'environnement.
- Cependant, après **200 000 parties**, le pourcentage de victoires diminue légèrement à **65.62%**.

###### **RANDOM commence :**
- Lorsque RANDOM commence, l'IA maintient une supériorité (jusqu'à 150 000 parties), bien que son taux de victoire soit plus faible qu'en jouant en premier.
- La performance augmente progressivement avec le nombre de parties, mais une baisse est observée à **200 000 parties** (**59.14%** → **58.60%**).

###### Pourquoi une baisse à 200 000 parties ?

1. *Surapprentissage :*
- À 200 000 parties, l'IA pourrait avoir surappris des stratégies spécifiques contre elle-même.  
- Contre un RANDOM, ces stratégies deviennent moins efficaces.

2. *Impact d'une exploration insuffisante :*
- L'IA, s'étant principalement entraînée contre elle-même, pourrait ne pas avoir exploré tous les états possibles de l'environnement.  
- Cela peut limiter sa capacité à réagir efficacement à des scénarios inattendus.


###### Impact des hyperparamètres (Alpha et Gamma)

*Alpha (taux d'apprentissage, ici = 0.3)*
- **Effet :**
  - Un alpha élevé (comme 0.3) permet une adaptation rapide, mais cela peut aussi rendre l'apprentissage instable.
- **Dans ce cas :**  
  - Un alpha de 0.3 semble initialement efficace, mais pourrait contribuer au surapprentissage.

*Gamma (facteur d'actualisation, ici = 0.3)*
- **Effet :**
  - Un gamma faible (comme ici, 0.3) privilégie des récompenses immédiates, ce qui peut limiter l'optimisation globale des stratégies.
- **Dans ce cas :**  
  - Gamma = 0.3 pourrait limiter la capacité de l'IA à anticiper les conséquences de ses actions sur le long terme, surtout dans des scénarios avec un grand nombre de parties.

###### Conclusion

Cette IA apprend rapidement, mais son apprentissage privilégie les récompenses immédiates. Cela limite sa capacité à développer des stratégies à long terme, pourtant essentielles pour ce type de jeu. 
En conséquence, son taux de réussite reste plafonné sous les 70 %.

La baisse des performances à 200 000 parties peut être expliquée par plusieurs facteurs combinés :

1. **Limitations des hyperparamètres :**

- Un alpha élevé (taux d'apprentissage) favorise des ajustements rapides mais peut provoquer une instabilité ou un surapprentissage.
- Un gamma faible (facteur d'actualisation) empêche l'IA d'optimiser les actions sur le long terme, en limitant son anticipation des récompenses différées.

2. **Manque de diversité dans l'entraînement :**

- En s'entraînant principalement contre elle-même, l'IA n'a pas exploré une variété suffisante de stratégies adverses.
- Cette homogénéité d'entraînement réduit sa capacité d'adaptation face à des scénarios imprévus ou à des adversaires adoptant des comportements aléatoires (RANDOM).

---
#### **Gamma = 0.9, Alpha = 0.9** (IA3)

##### 50 000
###### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 871             | 4129           |
| Games lost      | 4129            | 871            |
| Win percentage  | 17.42%          | 82.58%         |
| Lose percentage | 82.58%          | 17.42%         |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1908            | 3092           |
| Games lost      | 3092            | 1908           |
| Win percentage  | 38.16%          | 61.84%         |
| Lose percentage | 61.84%          | 38.16%         |

**BEST AI : AI**

##### 100 000
###### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1509            | 3491           |
| Games lost      | 3491            | 1509           |
| Win percentage  | 30.18%          | 69.82%         |
| Lose percentage | 69.82%          | 30.18%         |

**BEST AI : AI**

###### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1988            | 3012           |
| Games lost      | 3012            | 1988           |
| Win percentage  | 39.76%          | 60.24%         |
| Lose percentage | 60.24%          | 39.76%         |


**BEST AI : AI**

### 150 000
#### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1008            | 3992           |
| Games lost      | 3992            | 1008           |
| Win percentage  | 20.16%          | 79.84%         |
| Lose percentage | 79.84%          | 20.16%         |

**BEST AI : AI**

#### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1879            | 3121           |
| Games lost      | 3121            | 1879           |
| Win percentage  | 37.58%          | 62.42%         |
| Lose percentage | 62.42%          | 37.58%         |

**BEST AI : AI**


### 200 000
#### IA commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1353            | 3647           |
| Games lost      | 3647            | 1353           |
| Win percentage  | 27.06%          | 72.94%         |
| Lose percentage | 72.94%          | 27.06%         |

**BEST AI : AI**

#### RANDOM commence
| Metric          | RANDOM          | AI             |
|-----------------|-----------------|----------------|
| Games won       | 1884.0          | 3116           |
| Games lost      | 3116            | 1884.0         |
| Win percentage  | 37.68%          | 62.32%         |
| Lose percentage | 62.32%          | 37.68%         |


---
#### **Gamma = 0.9, Alpha = 0.1** (IA4)
##### 50 000
###### IA commence
|Metric              | RANDOM          | AI             |
|--------------------|-----------------|----------------|
| Games won          | 1652.0          | 3348           |
| Games lost         | 3348            | 1652.0         |
| Win percentage     | 33.04%          | 66.96%         |
| Lose percentage    | 66.96%          | 33.04%         |

**BEST AI : AI**

###### RANDOM commence 
|Metric              | RANDOM          | AI             |
|--------------------|-----------------|----------------|
| Games won          | 1981.0          | 3019           |
| Games lost         | 3019            | 1981.0         |
| Win percentage     | 39.62%          | 60.38%         |
| Lose percentage    | 60.38%          | 39.62%         |

**BEST AI : AI**

##### 100 000
###### IA commence 
|Metric              | RANDOM          | AI             |
|--------------------|-----------------|----------------|
| Games won          | 1185.0          | 3815           |
| Games lost         | 3815            | 1185.0         |
| Win percentage     | 23.70%          | 76.30%         |
| Lose percentage    | 76.30%          | 23.70%         |

**BEST AI : AI**

###### RANDOM commence 
|Metric              | RANDOM          | AI             |
|--------------------|-----------------|----------------|
| Games won          | 1871.0          | 3129           |
| Games lost         | 3129            | 1871.0         |
| Win percentage     | 37.42%          | 62.58%         |
| Lose percentage    | 62.58%          | 37.42%         |

**BEST AI : AI**

##### 150 000
###### IA commence 
|Metric              | RANDOM          | AI             |
|--------------------|-----------------|----------------|
| Games won          | 1088            | 3912           |
| Games lost         | 3912            | 1088           |
| Win percentage     | 21.76%          | 78.24%         |
| Lose percentage    | 78.24%          | 21.76%         |

**BEST AI : AI**

###### RANDOM commence 
|Metric              | RANDOM          | AI             |
|--------------------|-----------------|----------------|
| Games won          | 1880            | 3120           |
| Games lost         | 3120            | 1880           |
| Win percentage     | 37.6 %          | 62.4 %         |
| Lose percentage    | 62.40%          | 37.60%         |
**BEST AI : AI**

##### 200 000
*(Données manquantes)*
