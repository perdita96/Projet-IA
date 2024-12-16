## **Analyse comparative des IA**

### **Définition de la méthodologie**

Avant de procéder aux tests, il est essentiel de définir une méthodologie rigoureuse pour garantir des résultats pertinents. L'objectif est d'évaluer l'impact des hyperparamètres **Gamma** (facteur d'actualisation) et **Alpha** (facteur d'apprentissage) sur les performances des IA. Cette analyse se base sur trois configurations différentes de ces hyperparamètres, chacune visant à explorer des comportements d'apprentissage distincts.

---

### **Configurations testées**

Trois configurations de Gamma (facteur d'actualisation) et Alpha (facteur d'apprentissage) ont été définies. 
Chaque configuration est pensée pour représenter une stratégie d'apprentissage distincte, mettant en lumière les compromis entre récompenses immédiates et futures, ainsi que la vitesse d'intégration des nouvelles informations. Cette approche aide à mieux comprendre comment optimiser ces paramètres en fonction des objectifs du système.

1. **Gamma = 0.9, Alpha = 0.3**
2. **Gamma = 0.3, Alpha = 0.3**
3. **Gamma = 0.9, Alpha = 0.9**

si on a le temp
4. **Gamma = 0.9, Alpha = 0.1**

---

### **Méthodologie des tests**

Pour chaque configuration, un test sera exécutée afin d'évaluer les performances des IA dans un environnement standardisé. Les étapes suivantes seront respectées :  
1. **Définir des métriques d'évaluation** : le taux de victoire contre une IA random.
2. **Exécuter un nombre suffisant de parties** : nous avons choisis d'entrainer nos IA sur 200 000 parties par palier de 50 000
3. **Evlotution du epsilon**: nous avons choisit de diminuer de 1% toutes les 500 parties
3. **Test des IA** : nous avons choisis d'évaluer les IA sur 10 000 parties toutes les 50 000 parties
---

### **Conclusions attendues**

En analysant les résultats obtenus, il sera possible de :
- Identifier la configuration la plus adaptée au jeu étudié.
- Comprendre l’impact de chaque hyperparamètre sur les performances de l’IA.
- Adapter les choix d’hyperparamètres pour optimiser l’apprentissage en fonction des objectifs du jeu.

Les conclusions détaillées seront fournies après l’exécution des tests et l’analyse des résultats.
