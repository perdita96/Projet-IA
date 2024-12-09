## **Analyse comparative des IA**

### **Définition de la méthodologie**

Avant de procéder aux tests, il est essentiel de définir une méthodologie rigoureuse pour garantir des résultats pertinents. L'objectif est d'évaluer l'impact des hyperparamètres **Gamma** (facteur d'actualisation) et **Alpha** (facteur d'apprentissage) sur les performances des IA. Cette analyse se base sur trois configurations différentes de ces hyperparamètres, chacune visant à explorer des comportements d'apprentissage distincts.

---

### **Configurations testées**

les performances de l'IA, trois configurations de Gamma (facteur d'actualisation) et Alpha (facteur d'apprentissage) ont été définies. Ces choix permettent d'évaluer une large gamme de scénarios, allant d'un apprentissage lent et équilibré à une adaptation rapide et agressive. Chaque configuration est pensée pour représenter une stratégie d'apprentissage distincte, mettant en lumière les compromis entre récompenses immédiates et futures, ainsi que la vitesse d'intégration des nouvelles informations. Cette approche aide à mieux comprendre comment optimiser ces paramètres en fonction des objectifs du système.

#### **1. Gamma = 0.9, Alpha = 0.3**
- **Description** : Cette configuration vise un équilibre entre les récompenses futures et immédiates, tout en adoptant un apprentissage modéré.
- **Gamma = 0.9** : Met l'accent sur une planification à long terme, donnant beaucoup d'importance aux récompenses futures.
- **Alpha = 0.3** : Permet une intégration progressive des nouvelles informations, réduisant le risque de surajustement et favorisant la stabilité.

#### **2. Gamma = 0.3, Alpha = 0.3**
- **Description** : Cette configuration privilégie les récompenses immédiates, tout en maintenant un apprentissage modéré.
- **Gamma = 0.3** : Réduit considérablement l'importance des récompenses futures, poussant l'IA à se concentrer sur les gains immédiats.
- **Alpha = 0.3** : Assure un apprentissage modéré, évitant une adaptation trop rapide et garantissant une certaine robustesse.

#### **3. Gamma = 0.9, Alpha = 0.9**
- **Description** : Cette configuration favorise une planification à long terme combinée à un apprentissage rapide.
- **Gamma = 0.9** : Incite l'IA à prendre en compte les récompenses futures, favorisant des décisions optimales à long terme.
- **Alpha = 0.9** : Permet une adaptation rapide aux nouvelles expériences, mais avec le risque de perdre en stabilité si les informations anciennes sont rapidement oubliées.

---

### **Méthodologie des tests**

Pour chaque configuration, une batterie de tests sera exécutée afin d'évaluer les performances des IA dans un environnement standardisé. Les étapes suivantes seront respectées :  
1. **Définir des métriques d'évaluation** : le taux de victoire contre une IA random.
2. **Utiliser des environnements identiques** : Chaque configuration sera testée dans le même environnement pour garantir des comparaisons équitables.
3. **Exécuter un nombre suffisant de parties** : Cela permettra de lisser les fluctuations dues à la variabilité des résultats. Nous avons choisis d'entrainer nos IA sur 200 000 parties et de l'évaluer sur 1000 parties 

---

### **Résumé des configurations**

| **Configuration**           | **Description**                                                         |
|------------------------------|-------------------------------------------------------------------------|
| **Gamma = 0.9, Alpha = 0.3** | Équilibre entre récompenses futures et immédiates avec un apprentissage modéré. |
| **Gamma = 0.3, Alpha = 0.3** | Récompenses immédiates avec apprentissage modéré.                       |
| **Gamma = 0.9, Alpha = 0.9** | Planification à long terme avec apprentissage rapide.                   |

---

### **Conclusions attendues**

En analysant les résultats obtenus, il sera possible de :
- Identifier la configuration la plus adaptée au jeu étudié.
- Comprendre l’impact de chaque hyperparamètre sur les performances de l’IA.
- Adapter les choix d’hyperparamètres pour optimiser l’apprentissage en fonction des objectifs du jeu.

Les conclusions détaillées seront fournies après l’exécution des tests et l’analyse des résultats.
