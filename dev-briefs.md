# Pré-briefs Développement Modules WePresta

> Briefs techniques rapides pour les 6 premiers modules (Phase 1 - Quick Wins)

---

## 1. RGPD Cookie Consent Pro

**Prix cible** : 79€ | **Temps estimé** : 1-2 semaines

### Fonctionnalités Principales

| Priorité | Fonctionnalité | Détail |
|----------|----------------|--------|
| P0 | Bannière personnalisable | Position (bottom, top, modal), couleurs, textes |
| P0 | Consentement granulaire | 4 catégories : Nécessaires, Fonctionnels, Analytics, Marketing |
| P0 | Blocage scripts avant consentement | GTM, GA4, Facebook Pixel, etc. |
| P0 | Stockage du consentement | Cookie + option BDD pour preuve légale |
| P1 | Google Consent Mode v2 | Signaux `ad_storage`, `analytics_storage`, etc. |
| P1 | Registre des consentements | Export CSV pour audit CNIL |
| P1 | Multi-langue | Détection auto + traductions personnalisables |
| P2 | Templates préconçus | 3-5 designs (minimal, CNIL-like, custom) |
| P2 | Scanner de cookies | Détection auto des cookies présents |

### Points Techniques Compliqués

1. **Blocage des scripts AVANT consentement**
   - Réécriture des `<script>` en `<script type="text/plain" data-cookiecategory="analytics">`
   - Hook sur `header` pour intercepter les scripts
   - Gestion des scripts inline vs externes
   - Cas GTM : bloquer le container entier ou juste les tags ?

2. **Google Consent Mode v2**
   - Doit être AVANT le chargement de gtag.js
   - États par défaut : `denied` → mise à jour dynamique
   - Test avec Google Tag Assistant

3. **Preuve de consentement (registre)**
   - UUID unique par visiteur
   - Timestamp + version des CGU
   - IP hashée (RGPD-compliant)
   - Rétention : combien de temps ? (3 ans ?)

### Points Importants

- ✅ **NE PAS** bloquer les cookies techniques (session, panier)
- ✅ Respecter les guidelines CNIL (refuser aussi facile qu'accepter)
- ✅ Le consentement doit être renouvelé tous les 13 mois max
- ✅ Compatible avec le cache (Varnish, CloudFlare, PageCache)
- ✅ Pas de "mur de cookies" (dark patterns interdits)

### Questions à Trancher

| # | Question | Options | Recommandation |
|---|----------|---------|----------------|
| 1 | Stockage consentement | Cookie seul / Cookie + BDD | **Cookie + BDD** (preuve légale) |
| 2 | Durée consentement | 6 mois / 13 mois | **13 mois** (max légal) |
| 3 | Mode dégradé sans JS | Tout bloquer / Tout autoriser | **Tout bloquer** (safe) |
| 4 | Scanner auto cookies | Inclus / Module séparé | **Inclus** (différenciant) |
| 5 | Intégration Axeptio/Tarteaucitron | Import config / Non | **Non** (on est concurrents) |

### Stack Technique

```
- Hooks : displayHeader, actionFrontControllerSetMedia
- JS : Vanilla JS (pas de jQuery), ~15Ko max
- Storage : Cookie HttpOnly + table ps_cookie_consent_log
- Admin : Controller Symfony + formulaire configuration
```

### Estimation Détaillée

| Tâche | Temps |
|-------|-------|
| Structure module + admin | 2j |
| Bannière front (HTML/CSS/JS) | 2j |
| Logique blocage scripts | 2j |
| Google Consent Mode v2 | 1j |
| Registre consentements | 1j |
| Tests multi-thèmes | 1j |
| Documentation | 0.5j |
| **Total** | **~10j** |

---

## 2. Smart Popup & Exit Intent

**Prix cible** : 69€ | **Temps estimé** : 1-2 semaines

### Fonctionnalités Principales

| Priorité | Fonctionnalité | Détail |
|----------|----------------|--------|
| P0 | Exit intent detection | Détection mouvement souris vers fermeture |
| P0 | Déclencheurs multiples | Temps (30s), scroll (50%), clic, page vue |
| P0 | Éditeur visuel | Drag & drop basique, pas besoin de code |
| P0 | Templates | 10+ designs responsive |
| P1 | Ciblage pages | Toutes / Catégorie / Produit / CMS |
| P1 | Fréquence affichage | 1x/session, 1x/jour, 1x/semaine |
| P1 | Mobile : scroll-up intent | Équivalent exit intent mobile |
| P2 | A/B Testing | 2 variantes, stats conversion |
| P2 | Intégration formulaire | Champ email → newsletter PrestaShop |

### Points Techniques Compliqués

1. **Exit Intent Algorithm**
   ```js
   // Desktop : mouvement rapide vers le haut + sortie viewport
   document.addEventListener('mouseout', (e) => {
     if (e.clientY < 10 && e.relatedTarget === null) {
       showPopup();
     }
   });
   // Mobile : scroll-up rapide après scroll-down
   ```

2. **Éditeur Drag & Drop**
   - Option A : Éditeur custom léger (+ simple, - flexible)
   - Option B : Intégration GrapesJS (+ puissant, + lourd)
   - **Recommandation** : Templates fixes + personnalisation couleurs/textes

3. **Performances**
   - Lazy load popup HTML/CSS
   - Ne pas charger si déjà vu (cookie check)
   - Images en WebP + lazy loading

### Points Importants

- ✅ **JAMAIS** sur mobile au chargement (Google pénalise)
- ✅ Délai minimum avant affichage (pas instantané)
- ✅ Bouton fermer VISIBLE et fonctionnel
- ✅ ESC pour fermer (accessibilité)
- ✅ Focus trap dans la popup (accessibilité)

### Questions à Trancher

| # | Question | Options | Recommandation |
|---|----------|---------|----------------|
| 1 | Éditeur | Templates fixes / Drag & drop | **Templates + custom colors** |
| 2 | Stockage stats | Table custom / Hook natif | **Table custom** |
| 3 | Images popup | Upload BO / URL externe | **Upload BO** |
| 4 | Exit intent mobile | Scroll-up / Timer seul | **Scroll-up** |
| 5 | Multi-popup | 1 active / Plusieurs | **1 à la fois** (UX) |

### Stack Technique

```
- Hooks : displayHeader, displayFooter
- JS : Vanilla JS, détection events, localStorage
- Admin : CRUD popups, éditeur inline, stats dashboard
- Templates : Twig partials, CSS variables pour theming
```

### Estimation Détaillée

| Tâche | Temps |
|-------|-------|
| Structure module + admin CRUD | 2j |
| Exit intent JS + triggers | 1.5j |
| Templates popup (10) | 2j |
| Éditeur personnalisation | 1.5j |
| Ciblage pages + fréquence | 1j |
| Stats dashboard | 1j |
| Tests + doc | 1j |
| **Total** | **~10j** |

---

## 3. Mentions Légales Auto Generator

**Prix cible** : 59€ | **Temps estimé** : 1 semaine

### Fonctionnalités Principales

| Priorité | Fonctionnalité | Détail |
|----------|----------------|--------|
| P0 | Formulaire wizard | Questions guidées pour générer les docs |
| P0 | 4 documents | Mentions légales, CGV, Confidentialité, Cookies |
| P0 | Variables dynamiques | {nom_société}, {siret}, {adresse}, etc. |
| P0 | Création pages CMS | Auto-création des pages dans PrestaShop |
| P1 | Multi-boutiques | Config différente par shop |
| P1 | Export PDF | Version imprimable/archivable |
| P2 | Détection type activité | Auto-entrepreneur, SARL, SAS → clauses adaptées |
| P2 | Mises à jour légales | Notification quand màj juridique |

### Points Techniques Compliqués

1. **Modèles juridiques**
   - Doit être rédigé/validé par un juriste (coût externe ?)
   - Variantes selon : B2C/B2B, type société, secteur
   - Clause droit de rétractation (14j) obligatoire B2C

2. **Variables et conditions**
   ```twig
   {% if company_type == 'auto_entrepreneur' %}
     Dispensé d'immatriculation au RCS...
   {% else %}
     RCS {{ rcs_city }} {{ rcs_number }}
   {% endif %}
   ```

3. **Synchronisation CMS**
   - Créer/mettre à jour les pages CMS sans écraser le contenu custom
   - Gestion des slugs et SEO meta

### Points Importants

- ✅ **DISCLAIMER** : "Ces documents sont fournis à titre indicatif..."
- ✅ Toujours inclure date de dernière mise à jour
- ✅ Lien vers module RGPD Cookie pour cohérence
- ✅ Mentions légales ≠ CGV (2 documents distincts)
- ✅ Clause médiation consommation obligatoire

### Questions à Trancher

| # | Question | Options | Recommandation |
|---|----------|---------|----------------|
| 1 | Rédaction juridique | Interne / Externe (avocat) | **Avocat** (sécurité) |
| 2 | Pages CMS | Créer nouvelles / Maj existantes | **Option au choix** |
| 3 | Historique versions | Oui / Non | **Oui** (preuve) |
| 4 | Secteurs spécifiques | Générique / Alimentaire, Cosmétique... | **Générique v1** |
| 5 | Langue documents | FR seul / Multi | **FR v1**, multi v2 |

### Stack Technique

```
- Admin : Wizard multi-étapes (Symfony Form)
- Templates : Twig avec variables
- Stockage : JSON config + génération HTML
- CMS : API native PrestaShop pour créer/update pages
```

### Estimation Détaillée

| Tâche | Temps |
|-------|-------|
| Structure module + wizard | 1.5j |
| Templates 4 documents | 1j (+ temps juriste externe) |
| Moteur génération | 1j |
| Intégration CMS | 0.5j |
| Export PDF | 0.5j |
| Tests + doc | 0.5j |
| **Total** | **~5j** (hors validation juridique) |

### ⚠️ Risque

La rédaction des modèles juridiques nécessite un **avocat ou juriste**. Budget externe estimé : 500-1000€.

---

## 4. Ultimate Banners & Sliders

**Prix cible** : 79€ | **Temps estimé** : 2 semaines

### Fonctionnalités Principales

| Priorité | Fonctionnalité | Détail |
|----------|----------------|--------|
| P0 | Slider responsive | Swipe mobile, autoplay, pagination |
| P0 | Bannières statiques | Image + lien, positions multiples |
| P0 | Upload images | Drag & drop, crop, resize auto |
| P0 | Positions hooks | Home, catégorie, produit, header, footer |
| P1 | Programmation | Date début/fin pour promos |
| P1 | Responsive images | Srcset, WebP auto |
| P2 | Vidéo background | YouTube embed ou MP4 |
| P2 | Éditeur texte overlay | Titre, CTA sur l'image |
| P2 | A/B Testing | 2 visuels, stats clics |

### Points Techniques Compliqués

1. **Librairie slider**
   - Option A : Swiper.js (populaire, 30Ko)
   - Option B : Splide.js (léger, 15Ko)
   - Option C : CSS-only (très léger, moins de features)
   - **Recommandation** : Splide.js (bon compromis)

2. **Gestion images responsive**
   ```html
   <picture>
     <source media="(max-width: 768px)" srcset="banner-mobile.webp">
     <source media="(min-width: 769px)" srcset="banner-desktop.webp">
     <img src="banner-desktop.jpg" alt="...">
   </picture>
   ```
   - Générer les variantes au upload (ImageMagick/GD)

3. **Performance**
   - Lazy loading natif (`loading="lazy"`)
   - Preload LCP image (first slide)
   - Critical CSS inline pour éviter CLS

### Points Importants

- ✅ **LCP** : La première image doit être preload (Core Web Vitals)
- ✅ **CLS** : Réserver l'espace (aspect-ratio) pour éviter le shift
- ✅ ALT obligatoire (accessibilité + SEO)
- ✅ Liens en `<a>` pas en JS (SEO)
- ✅ Autoplay : option pour désactiver (accessibilité)

### Questions à Trancher

| # | Question | Options | Recommandation |
|---|----------|---------|----------------|
| 1 | Lib slider | Swiper / Splide / Custom | **Splide** |
| 2 | Éditeur texte | Overlay simple / WYSIWYG | **Overlay simple** v1 |
| 3 | Génération images | À l'upload / À la volée | **À l'upload** |
| 4 | Format images | JPG+WebP / WebP seul | **JPG+WebP** (fallback) |
| 5 | Vidéos | YouTube only / + MP4 | **YouTube v1** |

### Stack Technique

```
- JS : Splide.js (~15Ko gzipped)
- Images : ImageMagick pour resize/WebP
- Hooks : displayHome, displayHeader, displayFooter, displayCategoryHeader
- Admin : CRUD sliders/bannières, upload zone, preview live
```

### Estimation Détaillée

| Tâche | Temps |
|-------|-------|
| Structure module + admin | 2j |
| Upload images + traitement | 1.5j |
| Intégration Splide + templates | 2j |
| Hooks multiples + positions | 1j |
| Programmation dates | 0.5j |
| Responsive + WebP | 1j |
| Tests multi-thèmes + doc | 2j |
| **Total** | **~10j** |

---

## 5. FAQ Accordion Pro

**Prix cible** : 49€ | **Temps estimé** : 1 semaine

### Fonctionnalités Principales

| Priorité | Fonctionnalité | Détail |
|----------|----------------|--------|
| P0 | Accordéon animé | Ouverture/fermeture smooth |
| P0 | CRUD questions/réponses | Back-office simple |
| P0 | Catégories FAQ | Grouper par thème |
| P0 | Rich Snippets FAQPage | Schema.org JSON-LD |
| P1 | FAQ par produit | Questions spécifiques sur fiche produit |
| P1 | Recherche instantanée | Filtrer les questions |
| P2 | FAQ par catégorie | Questions liées aux catégories |
| P2 | Import/Export CSV | Migration données |
| P2 | Stats consultations | Questions les plus vues |

### Points Techniques Compliqués

1. **Schema.org FAQPage**
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [{
       "@type": "Question",
       "name": "Question 1 ?",
       "acceptedAnswer": {
         "@type": "Answer",
         "text": "Réponse 1..."
       }
     }]
   }
   ```
   - Max ~10 questions par page (Google)
   - Pas de HTML complexe dans les réponses

2. **FAQ sur fiche produit**
   - Hook `displayProductExtraContent` ou custom
   - Relation many-to-many : FAQ ↔ Produits
   - Option "FAQ globales + FAQ spécifiques"

3. **Accessibilité accordéon**
   ```html
   <button aria-expanded="false" aria-controls="faq-1">Question ?</button>
   <div id="faq-1" hidden>Réponse...</div>
   ```
   - Navigation clavier (Tab, Enter, Espace)
   - `aria-expanded` mis à jour dynamiquement

### Points Importants

- ✅ Un seul accordéon ouvert à la fois (option)
- ✅ Animation CSS (pas JS) pour performance
- ✅ Contenu indexable (pas `display:none` au chargement pour SEO)
- ✅ Réponses avec WYSIWYG (liens, gras, listes)
- ✅ Ordre drag & drop des questions

### Questions à Trancher

| # | Question | Options | Recommandation |
|---|----------|---------|----------------|
| 1 | Multi-ouverture | Un seul / Plusieurs | **Option au choix** |
| 2 | FAQ produit | Hook natif / Tab custom | **Tab custom** |
| 3 | Rich snippets | Toutes pages / Page FAQ seule | **Page FAQ + optionnel produits** |
| 4 | Recherche | JS filter / Ajax search | **JS filter** (simple) |
| 5 | WYSIWYG réponses | TinyMCE / Simple textarea | **TinyMCE** |

### Stack Technique

```
- HTML : <details>/<summary> natif (fallback) + JS enhance
- CSS : Transitions height avec max-height trick
- Schema : JSON-LD injecté via displayHeader
- Admin : DataTables + drag & drop (SortableJS)
```

### Estimation Détaillée

| Tâche | Temps |
|-------|-------|
| Structure module + CRUD | 1.5j |
| Front accordéon + CSS | 1j |
| Schema.org JSON-LD | 0.5j |
| FAQ sur fiches produits | 1j |
| Recherche JS | 0.5j |
| Tests + doc | 0.5j |
| **Total** | **~5j** |

---

## 6. Contact Form Builder

**Prix cible** : 59€ | **Temps estimé** : 1-2 semaines

### Fonctionnalités Principales

| Priorité | Fonctionnalité | Détail |
|----------|----------------|--------|
| P0 | Éditeur formulaire | Ajouter/supprimer/ordonner champs |
| P0 | Types de champs | Text, email, tel, select, textarea, checkbox |
| P0 | Validation | Required, email format, min/max length |
| P0 | Email notification | Envoi au bon service |
| P1 | Champs conditionnels | Afficher si champ X = valeur Y |
| P1 | Pièces jointes | Upload fichiers (PDF, images) |
| P1 | Anti-spam | reCAPTCHA v3 ou honeypot |
| P2 | Formulaires multiples | Contact, SAV, Devis, etc. |
| P2 | Historique messages | Stockage BDD + dashboard |
| P2 | Auto-réponse | Email de confirmation au client |

### Points Techniques Compliqués

1. **Éditeur de formulaire**
   - Option A : Interface liste (+ simple)
   - Option B : Drag & drop visuel (+ sexy, + complexe)
   - **Recommandation** : Liste avec drag & drop pour l'ordre

2. **Champs conditionnels**
   ```js
   // Config JSON
   {
     "field_id": "subject",
     "show_if": {
       "field": "type",
       "operator": "equals",
       "value": "reclamation"
     }
   }
   ```
   - Évaluation côté JS (affichage) + côté PHP (validation)

3. **Sécurité uploads**
   - Whitelist extensions (pdf, jpg, png)
   - Scan antivirus ? (optionnel)
   - Taille max (5Mo ?)
   - Stockage : `/upload/contact/` hors webroot

4. **Routage emails**
   ```
   Type = SAV → sav@boutique.fr
   Type = Commercial → contact@boutique.fr
   Type = Partenariat → partenariat@boutique.fr
   ```

### Points Importants

- ✅ RGPD : Case opt-in newsletter (non cochée par défaut)
- ✅ Confirmation visuelle après envoi
- ✅ Protection CSRF token
- ✅ Rate limiting (max 5 envois/IP/heure)
- ✅ Logs des envois (debug)

### Questions à Trancher

| # | Question | Options | Recommandation |
|---|----------|---------|----------------|
| 1 | Éditeur | Liste / Drag & drop | **Liste + ordre drag** |
| 2 | Anti-spam | reCAPTCHA / Honeypot / Les deux | **Honeypot + reCAPTCHA option** |
| 3 | Stockage messages | BDD / Email seul | **BDD + Email** |
| 4 | Pièces jointes | Oui v1 / Non v1 | **Oui** (différenciant) |
| 5 | Champs custom | Types fixes / Types extensibles | **Types fixes v1** |

### Stack Technique

```
- Admin : FormBuilder Symfony, SortableJS pour ordre
- Front : Validation HTML5 + JS, fetch pour submit
- Email : Mail PrestaShop natif
- Storage : Table ps_contact_form_message
- Anti-spam : Honeypot field + reCAPTCHA v3 optionnel
```

### Estimation Détaillée

| Tâche | Temps |
|-------|-------|
| Structure module + admin | 1.5j |
| Éditeur champs + config | 2j |
| Front formulaire + validation | 1.5j |
| Envoi email + routage | 1j |
| Pièces jointes | 1j |
| Anti-spam | 0.5j |
| Historique messages | 1j |
| Tests + doc | 1j |
| **Total** | **~10j** |

---

# Récapitulatif Phase 1

| # | Module | Prix | Temps | Complexité | Dépendances |
|---|--------|------|-------|------------|-------------|
| 1 | RGPD Cookie Consent | 79€ | 10j | ⭐⭐⭐ | Google Consent Mode |
| 2 | Smart Popup | 69€ | 10j | ⭐⭐ | - |
| 3 | Mentions Légales | 59€ | 5j | ⭐⭐ | Juriste externe |
| 4 | Banners & Sliders | 79€ | 10j | ⭐⭐ | Splide.js |
| 5 | FAQ Accordion | 49€ | 5j | ⭐ | - |
| 6 | Contact Form | 59€ | 10j | ⭐⭐ | - |

**Total Phase 1** : ~50 jours de dev = **10 semaines**

---

# Checklist Avant Dev

Pour chaque module :

- [ ] Valider le brief avec les décisions
- [ ] Créer repo Git `wepresta-{module-slug}`
- [ ] Scaffold module PrestaShop 8/9 [[memory:12505958]]
- [ ] Définir structure BDD (tables, relations)
- [ ] Wireframes admin (Figma ou papier)
- [ ] Tests manuels sur Hummingbird + Classic
- [ ] Documentation utilisateur (MD → PDF)
- [ ] Capture vidéo démo (optionnel mais recommandé)

---

*Généré le 28/12/2024*

