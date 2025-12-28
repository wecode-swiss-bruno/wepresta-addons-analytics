# WePresta - Plan de Contenu Modules

> Structure de données pour le site web. Chaque module suit le même format que la page EAA Accessibility Checker.

---

## Structure d'un module

```yaml
module:
  slug: string                    # URL friendly
  badge: string | null            # Ex: "DEADLINE", "NOUVEAU", "BEST-SELLER"
  badge_date: string | null       # Ex: "28 June 2025"
  
  title: string                   # H1
  tagline: string                 # Sous-titre
  description: string             # Description complète (2-3 phrases)
  
  stats:                          # 3 stats max
    - value: string
      label: string
  
  price:
    amount: number
    currency: "€"
    billing: "HT · TVA applicable"
  
  license_options:
    sites: ["1 site", "5 sites", "25 sites", "100 sites"]
    duration: ["1 an", "À vie"]
  
  includes:                       # Liste des inclusions
    - string
  
  features:                       # 4-6 features
    - title: string
      description: string
  
  compatibility:
    prestashop: ["8.1", "8.2", "9.0"]
    php: ["8.1", "8.2", "8.3"]
    themes: ["Hummingbird", "Classic", "Tous thèmes"]
  
  faq:                            # 3-5 questions
    - question: string
      answer: string
  
  testimonial:
    quote: string
    author: string
    role: string
    company: string
  
  cta_final:
    title: string
    subtitle: string
    button: string
  
  seo:
    meta_title: string
    meta_description: string
    keywords: [string]
  
  category: string                # Pour le listing
  order: number                   # Ordre d'affichage
```

---

# Catégories

## juridique

```yaml
name: "Juridique & Conformité"
slug: "juridique"
description: "Modules pour la conformité légale : RGPD, mentions légales, CGV, accessibilité."
icon: "⚖️"
order: 1
```

## marketing

```yaml
name: "Marketing & Conversion"
slug: "marketing"
description: "Augmentez vos conversions avec des popups, emails de relance et preuves sociales."
icon: "📈"
order: 2
```

## seo

```yaml
name: "SEO & Visibilité"
slug: "seo"
description: "Optimisez votre référencement naturel et apparaissez en haut de Google."
icon: "🔍"
order: 3
```

## gestion

```yaml
name: "Gestion & Productivité"
slug: "gestion"
description: "Gagnez du temps avec des outils d'administration et de gestion avancés."
icon: "⚙️"
order: 4
```

## ventes

```yaml
name: "Ventes & Fidélisation"
slug: "ventes"
description: "Augmentez le panier moyen et fidélisez vos clients."
icon: "💰"
order: 5
```

## integrations

```yaml
name: "Intégrations & Marketplaces"
slug: "integrations"
description: "Connectez votre boutique à Google Shopping, Amazon et autres marketplaces."
icon: "🔌"
order: 6
```

---

# Modules

---

## rgpd-cookie-consent-pro

```yaml
slug: "rgpd-cookie-consent-pro"
badge: "OBLIGATOIRE"
badge_date: null

title: "RGPD Cookie Consent Pro"
tagline: "Le gestionnaire de cookies le plus complet pour PrestaShop"
description: "Respectez le RGPD et ePrivacy avec une solution élégante et personnalisable. Vos visiteurs choisissent leurs préférences de cookies, vous restez en conformité avec la législation européenne."

stats:
  - value: "100%"
    label: "Conforme RGPD"
  - value: "6"
    label: "Langues incluses"
  - value: "<2min"
    label: "Installation"

price:
  amount: 79
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Bannière personnalisable"
    description: "Couleurs, textes, position et animations entièrement configurables"
  - title: "Consentement granulaire"
    description: "Analytics, marketing, fonctionnel : vos visiteurs choisissent"
  - title: "Blocage automatique"
    description: "Scripts bloqués avant consentement, conformité garantie"
  - title: "Registre des consentements"
    description: "Preuve légale de chaque consentement pour vos audits"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le module bloque-t-il Google Analytics avant consentement ?"
    answer: "Oui, tous les scripts de tracking sont automatiquement bloqués jusqu'à ce que le visiteur donne son consentement explicite."
  - question: "Est-ce compatible avec Google Consent Mode v2 ?"
    answer: "Absolument. Le module envoie les signaux de consentement à Google pour optimiser vos campagnes publicitaires."
  - question: "Puis-je personnaliser les textes ?"
    answer: "Oui, tous les textes sont modifiables dans le back-office, en plusieurs langues."

testimonial:
  quote: "Enfin un module cookies qui ne casse pas le design de notre site. Installation en 5 minutes, configuration intuitive."
  author: "Marie L."
  role: "Responsable e-commerce"
  company: "BoutiqueMode.fr"

cta_final:
  title: "Soyez conforme dès aujourd'hui"
  subtitle: "Installez le module en quelques minutes et protégez votre boutique."
  button: "Acheter RGPD Cookie Consent Pro"

seo:
  meta_title: "RGPD Cookie Consent Pro | Module PrestaShop | WePresta"
  meta_description: "Gestionnaire de cookies RGPD pour PrestaShop. Bannière personnalisable, consentement granulaire, compatible Google Consent Mode v2."
  keywords: ["rgpd", "cookies", "prestashop", "gdpr", "consentement", "eprivacy"]

category: "juridique"
order: 1
```

---

## mentions-legales-generator

```yaml
slug: "mentions-legales-generator"
badge: null
badge_date: null

title: "Mentions Légales Auto Generator"
tagline: "Générez vos pages légales en 2 minutes"
description: "Plus besoin d'avocat pour vos mentions légales, CGV et politique de confidentialité. Répondez à quelques questions, obtenez des documents conformes et à jour."

stats:
  - value: "4"
    label: "Documents générés"
  - value: "2min"
    label: "Configuration"
  - value: "Auto"
    label: "Mises à jour légales"

price:
  amount: 59
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Générateur intelligent"
    description: "Mentions légales, CGV, confidentialité générés automatiquement"
  - title: "Conforme au droit français et européen"
    description: "Droit de rétractation, livraison, garanties inclus"
  - title: "Mises à jour automatiques"
    description: "Vos documents suivent les évolutions légales"
  - title: "Export PDF"
    description: "Archivez vos documents pour preuve légale"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les CGV sont-elles adaptées au e-commerce ?"
    answer: "Oui, elles incluent toutes les clauses obligatoires : droit de rétractation 14 jours, livraison, garanties légales, etc."
  - question: "Puis-je modifier les textes générés ?"
    answer: "Oui, les textes générés sont entièrement éditables dans le back-office."
  - question: "Le module gère-t-il le multi-boutiques ?"
    answer: "Oui, vous pouvez générer des documents différents pour chaque boutique."

testimonial:
  quote: "J'ai économisé 500€ de frais d'avocat. Les documents sont complets et professionnels."
  author: "Thomas R."
  role: "Gérant"
  company: "SportShop.fr"

cta_final:
  title: "Vos pages légales en 2 minutes"
  subtitle: "Répondez au questionnaire et obtenez vos documents conformes."
  button: "Acheter Mentions Légales Generator"

seo:
  meta_title: "Générateur Mentions Légales CGV | Module PrestaShop | WePresta"
  meta_description: "Générez automatiquement vos mentions légales, CGV et politique de confidentialité conformes pour PrestaShop."
  keywords: ["mentions légales", "cgv", "prestashop", "générateur", "legal"]

category: "juridique"
order: 2
```

---

## smart-popup-exit-intent

```yaml
slug: "smart-popup-exit-intent"
badge: "BEST-SELLER"
badge_date: null

title: "Smart Popup & Exit Intent"
tagline: "Capturez l'attention au bon moment"
description: "Popups intelligentes qui s'affichent au moment parfait : intention de sortie, scroll, temps passé. Augmentez vos conversions sans énerver vos visiteurs."

stats:
  - value: "+25%"
    label: "Conversions"
  - value: "15+"
    label: "Templates inclus"
  - value: "A/B"
    label: "Testing intégré"

price:
  amount: 69
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Exit Intent Detection"
    description: "Détecte quand le visiteur s'apprête à quitter la page"
  - title: "Déclencheurs multiples"
    description: "Scroll %, temps passé, clic, page spécifique"
  - title: "Éditeur drag & drop"
    description: "Créez des popups sans coder avec 15+ templates"
  - title: "A/B Testing"
    description: "Testez différentes versions et optimisez vos résultats"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les popups fonctionnent-elles sur mobile ?"
    answer: "Oui, les popups sont 100% responsives et optimisées pour tous les appareils."
  - question: "Puis-je cibler des pages spécifiques ?"
    answer: "Oui, vous pouvez afficher une popup uniquement sur certaines catégories, produits ou pages CMS."
  - question: "Le module ralentit-il le site ?"
    answer: "Non, le script est chargé de manière asynchrone et pèse moins de 15 Ko."

testimonial:
  quote: "Notre taux de capture email est passé de 2% à 8% grâce à la popup exit intent. ROI immédiat."
  author: "Sophie M."
  role: "Marketing Manager"
  company: "BeautyStore.fr"

cta_final:
  title: "Convertissez plus de visiteurs"
  subtitle: "Installez le module et créez votre première popup en 5 minutes."
  button: "Acheter Smart Popup"

seo:
  meta_title: "Popup Exit Intent PrestaShop | Module | WePresta"
  meta_description: "Module popup exit intent pour PrestaShop. Augmentez vos conversions avec des popups intelligentes et personnalisables."
  keywords: ["popup", "exit intent", "prestashop", "conversion", "marketing"]

category: "marketing"
order: 1
```

---

## newsletter-subscription

```yaml
slug: "newsletter-subscription"
badge: null
badge_date: null

title: "Newsletter Popup & Subscription"
tagline: "Construisez votre liste email qui convertit"
description: "Transformez chaque visiteur en abonné avec des formulaires optimisés. Intégration directe avec Mailchimp, Sendinblue, Klaviyo et +20 services."

stats:
  - value: "20+"
    label: "Intégrations"
  - value: "RGPD"
    label: "Double opt-in"
  - value: "Auto"
    label: "Code promo"

price:
  amount: 69
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Popup d'inscription élégante"
    description: "Designs modernes et personnalisables pour maximiser les conversions"
  - title: "Intégrations multiples"
    description: "Mailchimp, Sendinblue, Klaviyo, Mailjet et 20+ services"
  - title: "Code promo automatique"
    description: "Offrez une réduction en échange de l'inscription"
  - title: "Double opt-in RGPD"
    description: "Conformité garantie avec email de confirmation"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Quels services email sont compatibles ?"
    answer: "Mailchimp, Sendinblue, Klaviyo, Mailjet, ActiveCampaign, GetResponse, et plus de 15 autres services via API ou webhook."
  - question: "Puis-je segmenter les abonnés ?"
    answer: "Oui, vous pouvez ajouter des tags automatiques selon la source d'inscription ou les préférences du visiteur."
  - question: "Le code promo est-il personnalisé par visiteur ?"
    answer: "Oui, vous pouvez générer des codes uniques ou utiliser un code fixe."

testimonial:
  quote: "Notre liste email a doublé en 3 mois. L'intégration Klaviyo fonctionne parfaitement."
  author: "Lucas D."
  role: "Fondateur"
  company: "TechGadgets.fr"

cta_final:
  title: "Développez votre liste email"
  subtitle: "Chaque abonné est un futur client. Commencez à collecter."
  button: "Acheter Newsletter Subscription"

seo:
  meta_title: "Newsletter Popup PrestaShop | Mailchimp Sendinblue | WePresta"
  meta_description: "Module newsletter pour PrestaShop avec intégration Mailchimp, Sendinblue, Klaviyo. Popup d'inscription et double opt-in RGPD."
  keywords: ["newsletter", "prestashop", "mailchimp", "sendinblue", "popup", "email"]

category: "marketing"
order: 2
```

---

## social-proof-notifications

```yaml
slug: "social-proof-notifications"
badge: null
badge_date: null

title: "Social Proof Notifications"
tagline: "Marie vient d'acheter ce produit"
description: "Créez un sentiment d'urgence et de confiance avec des notifications en temps réel. Montrez que d'autres achètent, et convertissez les hésitants."

stats:
  - value: "+15%"
    label: "Taux de conversion"
  - value: "Real-time"
    label: "Notifications"
  - value: "RGPD"
    label: "Anonymisation"

price:
  amount: 79
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Notifications de ventes"
    description: "Affichez les achats récents en temps réel"
  - title: "Alertes stock faible"
    description: "Plus que 3 en stock - créez l'urgence"
  - title: "Compteur visiteurs actifs"
    description: "12 personnes regardent ce produit"
  - title: "Mode simulation"
    description: "Idéal pour les nouvelles boutiques sans historique"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les données affichées sont-elles réelles ?"
    answer: "Par défaut oui, mais vous pouvez activer le mode simulation pour les nouvelles boutiques."
  - question: "Est-ce conforme au RGPD ?"
    answer: "Oui, les noms sont anonymisés (Marie L. de Paris) et aucune donnée personnelle n'est exposée."
  - question: "Puis-je personnaliser le design ?"
    answer: "Oui, position, couleurs, animations et délais sont entièrement configurables."

testimonial:
  quote: "L'effet FOMO fonctionne vraiment. Nos conversions ont augmenté de 18% le premier mois."
  author: "Pierre B."
  role: "CEO"
  company: "MaisonDeco.fr"

cta_final:
  title: "Créez l'urgence qui convertit"
  subtitle: "Montrez à vos visiteurs qu'ils ne sont pas seuls."
  button: "Acheter Social Proof"

seo:
  meta_title: "Social Proof Notifications PrestaShop | FOMO | WePresta"
  meta_description: "Module social proof pour PrestaShop. Notifications d'achats en temps réel, compteur visiteurs, alertes stock. Augmentez vos conversions."
  keywords: ["social proof", "fomo", "prestashop", "notifications", "conversion"]

category: "marketing"
order: 3
```

---

## cart-recovery-email

```yaml
slug: "cart-recovery-email"
badge: "ROI GARANTI"
badge_date: null

title: "Smart Cart Recovery Email"
tagline: "Récupérez 15-30% des paniers abandonnés"
description: "Séquences d'emails automatiques pour relancer les clients qui n'ont pas finalisé leur achat. Personnalisation avancée et timing optimisé par IA."

stats:
  - value: "15-30%"
    label: "Paniers récupérés"
  - value: "3"
    label: "Emails automatiques"
  - value: "A/B"
    label: "Testing inclus"

price:
  amount: 169
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Séquences automatiques"
    description: "3 emails programmés : 1h, 24h et 72h après abandon"
  - title: "Contenu dynamique"
    description: "Produits du panier inclus automatiquement dans l'email"
  - title: "Code promo progressif"
    description: "5% au 1er email, 10% au 2ème, 15% au 3ème"
  - title: "Dashboard de performance"
    description: "Taux d'ouverture, clics, conversions en temps réel"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Faut-il un service d'email externe ?"
    answer: "Non, le module peut envoyer via le SMTP de PrestaShop. Mais nous recommandons Sendinblue ou Mailjet pour de meilleurs taux de délivrabilité."
  - question: "Les emails sont-ils conformes RGPD ?"
    answer: "Oui, chaque email inclut un lien de désinscription et nous ne contactons que les clients ayant accepté les communications."
  - question: "Puis-je personnaliser les templates ?"
    answer: "Oui, chaque email est entièrement personnalisable via un éditeur visuel."

testimonial:
  quote: "On récupère environ 2000€/mois de paniers abandonnés. Le module s'est rentabilisé en 3 jours."
  author: "Antoine G."
  role: "Directeur e-commerce"
  company: "OutdoorShop.fr"

cta_final:
  title: "Arrêtez de perdre des ventes"
  subtitle: "Chaque panier abandonné est une opportunité. Récupérez-les."
  button: "Acheter Cart Recovery"

seo:
  meta_title: "Relance Panier Abandonné PrestaShop | Email Automatique | WePresta"
  meta_description: "Module de relance panier abandonné pour PrestaShop. Séquences email automatiques, codes promo progressifs. Récupérez 15-30% des paniers."
  keywords: ["panier abandonné", "prestashop", "email", "relance", "cart recovery"]

category: "marketing"
order: 4
```

---

## product-reviews-ratings

```yaml
slug: "product-reviews-ratings"
badge: null
badge_date: null

title: "Product Reviews & Ratings"
tagline: "Les avis qui font vendre"
description: "Collectez et affichez les avis clients pour booster la confiance et le SEO. Intégration Google Shopping pour les rich snippets étoilés."

stats:
  - value: "⭐⭐⭐⭐⭐"
    label: "Rich Snippets"
  - value: "Auto"
    label: "Collecte post-achat"
  - value: "Photo"
    label: "Avis avec images"

price:
  amount: 89
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Collecte automatique"
    description: "Email de demande d'avis envoyé après livraison"
  - title: "Avis avec photos"
    description: "Vos clients peuvent ajouter des images à leurs avis"
  - title: "Rich Snippets Google"
    description: "Étoiles affichées dans les résultats de recherche"
  - title: "Modération facile"
    description: "Approuvez, répondez et gérez tous vos avis"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les étoiles apparaissent-elles dans Google ?"
    answer: "Oui, le module génère les balises Schema.org nécessaires pour afficher les étoiles dans les résultats de recherche."
  - question: "Puis-je importer mes avis existants ?"
    answer: "Oui, vous pouvez importer des avis depuis un fichier CSV ou depuis le module natif PrestaShop."
  - question: "Comment éviter les faux avis ?"
    answer: "Le module vérifie que l'auteur a bien acheté le produit avant de publier l'avis."

testimonial:
  quote: "Nos fiches produits avec avis convertissent 40% mieux que celles sans. Indispensable."
  author: "Claire V."
  role: "Product Manager"
  company: "KidsStore.fr"

cta_final:
  title: "La confiance qui convertit"
  subtitle: "Chaque avis est une preuve sociale. Collectez-les automatiquement."
  button: "Acheter Product Reviews"

seo:
  meta_title: "Avis Clients PrestaShop | Rich Snippets Google | WePresta"
  meta_description: "Module avis clients pour PrestaShop avec rich snippets Google. Collecte automatique, modération, avis avec photos."
  keywords: ["avis", "reviews", "prestashop", "rich snippets", "étoiles", "google"]

category: "marketing"
order: 5
```

---

## seo-manager-360

```yaml
slug: "seo-manager-360"
badge: null
badge_date: null

title: "SEO Manager 360"
tagline: "Votre expert SEO intégré à PrestaShop"
description: "Audit, optimisation et suivi SEO complet. Corrigez les erreurs, optimisez vos contenus, et grimpez dans Google avec des recommandations concrètes."

stats:
  - value: "100+"
    label: "Points d'audit"
  - value: "IA"
    label: "Génération meta"
  - value: "GSC"
    label: "Intégration"

price:
  amount: 149
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Audit SEO complet"
    description: "Analyse automatique de toutes vos pages avec score et recommandations"
  - title: "Optimisation meta en masse"
    description: "Modifiez titles et descriptions de centaines de produits en un clic"
  - title: "Générateur IA"
    description: "Génération automatique de meta descriptions optimisées"
  - title: "Intégration Search Console"
    description: "Données de performance directement dans PrestaShop"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le module génère-t-il un sitemap ?"
    answer: "Oui, un sitemap XML optimisé est généré automatiquement et soumis à Google."
  - question: "Puis-je gérer les redirections 301 ?"
    answer: "Oui, un gestionnaire de redirections est inclus pour ne jamais perdre de jus SEO."
  - question: "L'IA consomme-t-elle des crédits ?"
    answer: "Non, la génération IA est incluse sans limite dans votre licence."

testimonial:
  quote: "Notre trafic organique a augmenté de 180% en 6 mois. L'audit a révélé des erreurs qu'on ignorait."
  author: "Marc D."
  role: "SEO Manager"
  company: "ElectroShop.fr"

cta_final:
  title: "Dominez les résultats Google"
  subtitle: "Un SEO optimisé = du trafic gratuit. Commencez l'audit."
  button: "Acheter SEO Manager 360"

seo:
  meta_title: "Module SEO PrestaShop | Audit & Optimisation | WePresta"
  meta_description: "Module SEO complet pour PrestaShop. Audit automatique, optimisation meta, génération IA, intégration Google Search Console."
  keywords: ["seo", "prestashop", "référencement", "audit", "meta", "google"]

category: "seo"
order: 1
```

---

## rich-snippets-schema

```yaml
slug: "rich-snippets-schema"
badge: null
badge_date: null

title: "Rich Snippets & Schema Pro"
tagline: "Démarquez-vous dans les résultats Google"
description: "Ajoutez les données structurées Schema.org pour afficher prix, avis, stock directement dans Google. Multipliez votre CTR par 2."

stats:
  - value: "x2"
    label: "CTR moyen"
  - value: "JSON-LD"
    label: "Format moderne"
  - value: "Auto"
    label: "Validation Google"

price:
  amount: 99
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Schema Product"
    description: "Prix, disponibilité, avis affichés dans Google"
  - title: "Schema Organization"
    description: "Informations entreprise et logo dans les résultats"
  - title: "Schema FAQ"
    description: "Questions/réponses déployées directement dans Google"
  - title: "Validation intégrée"
    description: "Vérifiez que vos données sont correctement interprétées"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Quelle est la différence avec le SEO Manager ?"
    answer: "Le SEO Manager gère le contenu (meta, sitemap). Rich Snippets gère les données structurées pour l'affichage enrichi dans Google."
  - question: "Les rich snippets sont-ils garantis ?"
    answer: "Google décide d'afficher ou non les rich snippets. Le module garantit que les données sont correctement formatées pour maximiser vos chances."
  - question: "Le module ralentit-il le site ?"
    answer: "Non, les données Schema sont générées côté serveur et ajoutent moins de 1 Ko au HTML."

testimonial:
  quote: "Nos produits se démarquent enfin dans Google. Le CTR a doublé sur nos mots-clés principaux."
  author: "Julie T."
  role: "Responsable acquisition"
  company: "JardinShop.fr"

cta_final:
  title: "Brillez dans Google"
  subtitle: "Des résultats enrichis = plus de clics. Installez Schema Pro."
  button: "Acheter Rich Snippets"

seo:
  meta_title: "Rich Snippets PrestaShop | Schema.org | WePresta"
  meta_description: "Module rich snippets pour PrestaShop. Données structurées Schema.org, étoiles dans Google, prix et stock affichés."
  keywords: ["rich snippets", "schema", "prestashop", "structured data", "google"]

category: "seo"
order: 2
```

---

## advanced-product-filters

```yaml
slug: "advanced-product-filters"
badge: "POPULAIRE"
badge_date: null

title: "Advanced Product Filters"
tagline: "Trouvez le bon produit en 2 clics"
description: "Filtres avancés pour gros catalogues. Ajax sans rechargement, multi-critères, et UX optimisée pour mobile. Vos clients trouvent ce qu'ils cherchent."

stats:
  - value: "Ajax"
    label: "Sans rechargement"
  - value: "SEO"
    label: "URLs propres"
  - value: "Mobile"
    label: "Optimisé"

price:
  amount: 149
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Filtres Ajax"
    description: "Résultats instantanés sans rechargement de page"
  - title: "Filtres visuels"
    description: "Couleurs en pastilles, tailles avec icônes"
  - title: "SEO-friendly"
    description: "URLs propres indexables par Google"
  - title: "Performance"
    description: "Cache intelligent pour des réponses ultra-rapides"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le module remplace-t-il les filtres natifs ?"
    answer: "Oui, il remplace et améliore considérablement les filtres de PrestaShop."
  - question: "Fonctionne-t-il avec les gros catalogues ?"
    answer: "Oui, le module est optimisé pour les catalogues de 10 000+ produits grâce au cache."
  - question: "Les URLs filtrées sont-elles indexées ?"
    answer: "Vous pouvez choisir quelles combinaisons de filtres indexer pour éviter le duplicate content."

testimonial:
  quote: "Nos clients trouvent leurs produits 3x plus vite. Le taux de rebond a chuté de 40%."
  author: "Olivier R."
  role: "CTO"
  company: "PiecesAuto.fr"

cta_final:
  title: "Une recherche qui convertit"
  subtitle: "Si vos clients ne trouvent pas, ils partent. Donnez-leur les bons outils."
  button: "Acheter Advanced Filters"

seo:
  meta_title: "Filtres Produits Ajax PrestaShop | Module | WePresta"
  meta_description: "Module de filtres produits avancés pour PrestaShop. Ajax, filtres visuels, SEO-friendly. Optimisé pour les gros catalogues."
  keywords: ["filtres", "prestashop", "ajax", "faceted", "navigation", "recherche"]

category: "gestion"
order: 1
```

---

## google-shopping-feed

```yaml
slug: "google-shopping-feed"
badge: "TOP VENTES"
badge_date: null

title: "Google Shopping Feed Pro"
tagline: "Vos produits en haut de Google"
description: "Feed produits optimisé pour Google Merchant Center. Performance Max, Shopping Ads, et comparateurs de prix. Synchronisation automatique."

stats:
  - value: "Auto"
    label: "Synchronisation"
  - value: "Multi"
    label: "Langues & devises"
  - value: "GMC"
    label: "100% compatible"

price:
  amount: 179
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Feed optimisé Google"
    description: "Format XML conforme aux exigences Merchant Center"
  - title: "Optimisation des titres"
    description: "Enrichissement automatique avec marque, couleur, taille"
  - title: "Gestion des variantes"
    description: "Chaque déclinaison exportée correctement"
  - title: "Multi-pays"
    description: "Un feed par langue et devise pour vos marchés"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le feed est-il automatiquement mis à jour ?"
    answer: "Oui, le feed se régénère automatiquement selon la fréquence que vous choisissez (horaire, quotidien)."
  - question: "Puis-je exclure certains produits ?"
    answer: "Oui, via des règles (catégorie, stock, marge minimum) ou manuellement."
  - question: "Le module gère-t-il les promotions ?"
    answer: "Oui, les prix barrés et promotions sont automatiquement inclus dans le feed."

testimonial:
  quote: "Notre ROAS Google Shopping a augmenté de 35% grâce à l'optimisation des titres."
  author: "Nicolas P."
  role: "Traffic Manager"
  company: "SportEquip.fr"

cta_final:
  title: "Vendez sur Google Shopping"
  subtitle: "Des millions de recherches produits chaque jour. Soyez visible."
  button: "Acheter Google Shopping Feed"

seo:
  meta_title: "Google Shopping Feed PrestaShop | Merchant Center | WePresta"
  meta_description: "Module Google Shopping pour PrestaShop. Feed XML optimisé, synchronisation automatique, gestion multi-pays."
  keywords: ["google shopping", "prestashop", "feed", "merchant center", "pla"]

category: "integrations"
order: 1
```

---

## amazon-marketplace-connector

```yaml
slug: "amazon-marketplace-connector"
badge: "PREMIUM"
badge_date: null

title: "Amazon Marketplace Connector"
tagline: "Vendez sur Amazon depuis PrestaShop"
description: "Synchronisation bi-directionnelle complète : produits, stocks, commandes, prix. Gérez tout depuis un seul back-office. Support FBA inclus."

stats:
  - value: "Bi-dir"
    label: "Synchronisation"
  - value: "5"
    label: "Pays Amazon"
  - value: "FBA"
    label: "Support inclus"

price:
  amount: 249
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Export catalogue"
    description: "Envoyez vos produits sur Amazon en quelques clics"
  - title: "Synchro stocks temps réel"
    description: "Évitez les surventes avec une synchronisation bidirectionnelle"
  - title: "Import commandes"
    description: "Toutes vos commandes Amazon centralisées dans PrestaShop"
  - title: "Support FBA"
    description: "Gérez vos produits Fulfillment by Amazon"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Quels pays Amazon sont supportés ?"
    answer: "France, Allemagne, Espagne, Italie, UK, et bientôt USA."
  - question: "Le module gère-t-il les variantes ?"
    answer: "Oui, les produits avec déclinaisons sont correctement mappés vers les variantes Amazon."
  - question: "Puis-je avoir des prix différents sur Amazon ?"
    answer: "Oui, vous pouvez définir une marge ou un prix fixe différent pour Amazon."

testimonial:
  quote: "On gère 3000 commandes/mois entre PrestaShop et Amazon sans aucune erreur de stock."
  author: "David M."
  role: "COO"
  company: "MegaStore.fr"

cta_final:
  title: "Vendez sur Amazon sans effort"
  subtitle: "Le plus grand marketplace du monde, depuis votre PrestaShop."
  button: "Acheter Amazon Connector"

seo:
  meta_title: "Connecteur Amazon PrestaShop | Sync Produits Commandes | WePresta"
  meta_description: "Module Amazon pour PrestaShop. Synchronisation produits, stocks, commandes. Support multi-pays et FBA."
  keywords: ["amazon", "prestashop", "marketplace", "connector", "sync", "fba"]

category: "integrations"
order: 2
```

---

## oss-vat-manager

```yaml
slug: "oss-vat-manager"
badge: "OBLIGATION EU"
badge_date: null

title: "OSS VAT Manager"
tagline: "Gérez la TVA européenne automatiquement"
description: "Calculez et appliquez automatiquement les taux de TVA selon le pays du client. Conforme au régime OSS (One-Stop-Shop) obligatoire depuis juillet 2021."

stats:
  - value: "27"
    label: "Pays EU"
  - value: "Auto"
    label: "Détection pays"
  - value: "OSS"
    label: "100% conforme"

price:
  amount: 129
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Taux TVA automatiques"
    description: "Tous les taux de l'UE pré-configurés et mis à jour"
  - title: "Détection géographique"
    description: "Le bon taux appliqué selon l'IP ou l'adresse du client"
  - title: "Rapports OSS"
    description: "Export des ventes par pays pour votre déclaration"
  - title: "Multi-boutiques"
    description: "Configuration différente par boutique si nécessaire"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le module gère-t-il le B2B avec numéro de TVA ?"
    answer: "Oui, les clients B2B avec numéro de TVA valide peuvent bénéficier de l'exonération."
  - question: "Les taux sont-ils mis à jour automatiquement ?"
    answer: "Oui, nous mettons à jour les taux à chaque changement de législation."
  - question: "Le module fonctionne-t-il hors UE ?"
    answer: "Oui, vous pouvez configurer des règles pour la Suisse, UK et autres pays."

testimonial:
  quote: "Fini le casse-tête de la TVA OSS. Le module gère tout automatiquement."
  author: "Philippe G."
  role: "Gérant"
  company: "EuroShop.fr"

cta_final:
  title: "La TVA OSS sans stress"
  subtitle: "Restez conforme à la législation européenne automatiquement."
  button: "Acheter OSS VAT Manager"

seo:
  meta_title: "OSS TVA PrestaShop | One-Stop-Shop | WePresta"
  meta_description: "Module TVA OSS pour PrestaShop. Calcul automatique des taux européens, rapports pour déclaration, détection géographique."
  keywords: ["oss", "tva", "prestashop", "vat", "europe", "ioss"]

category: "juridique"
order: 3
```

---

## gpsr-compliance

```yaml
slug: "gpsr-compliance"
badge: "DEADLINE"
badge_date: "13 December 2024"

title: "GPSR Compliance"
tagline: "Conformité au règlement européen sur la sécurité des produits"
description: "Affichez les informations fabricant obligatoires sur vos fiches produits. Conforme au GPSR (General Product Safety Regulation) entré en vigueur le 13 décembre 2024."

stats:
  - value: "GPSR"
    label: "100% conforme"
  - value: "Auto"
    label: "Affichage champs"
  - value: "Import"
    label: "CSV inclus"

price:
  amount: 89
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Champs fabricant"
    description: "Nom, adresse, email du fabricant/importateur sur chaque produit"
  - title: "Import en masse"
    description: "Importez les données fabricant via CSV pour tout votre catalogue"
  - title: "Affichage automatique"
    description: "Les informations s'affichent automatiquement sur les fiches"
  - title: "Gestion par catégorie"
    description: "Définissez un fabricant par défaut par catégorie"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Qui est concerné par le GPSR ?"
    answer: "Tous les vendeurs qui commercialisent des produits dans l'UE, qu'ils soient fabricants, importateurs ou distributeurs."
  - question: "Quelles informations sont obligatoires ?"
    answer: "Nom et adresse postale du fabricant ou de l'importateur, et un moyen de contact."
  - question: "Puis-je avoir un fabricant différent par produit ?"
    answer: "Oui, vous pouvez définir les informations au niveau du produit ou par défaut au niveau catégorie."

testimonial:
  quote: "On a mis à jour nos 2000 produits en une heure grâce à l'import CSV. Indispensable."
  author: "Sarah M."
  role: "Responsable catalogue"
  company: "GadgetStore.fr"

cta_final:
  title: "Soyez conforme au GPSR"
  subtitle: "La deadline est passée. Mettez-vous en conformité maintenant."
  button: "Acheter GPSR Compliance"

seo:
  meta_title: "GPSR Compliance PrestaShop | Règlement Sécurité Produits | WePresta"
  meta_description: "Module GPSR pour PrestaShop. Affichez les informations fabricant obligatoires. Import CSV, gestion par catégorie."
  keywords: ["gpsr", "prestashop", "sécurité produits", "fabricant", "importateur"]

category: "juridique"
order: 4
```

---

## picking-list-pro

```yaml
slug: "picking-list-pro"
badge: null
badge_date: null

title: "Picking List Pro"
tagline: "Préparez vos commandes 2x plus vite"
description: "Générez des listes de picking optimisées pour votre entrepôt. Regroupement par emplacement, codes-barres, validation scan. Gagnez du temps sur chaque commande."

stats:
  - value: "x2"
    label: "Plus rapide"
  - value: "Scan"
    label: "Validation"
  - value: "PDF"
    label: "Export"

price:
  amount: 129
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Tri par emplacement"
    description: "Les produits triés selon leur position dans l'entrepôt"
  - title: "Regroupement multi-commandes"
    description: "Préparez plusieurs commandes en un seul passage"
  - title: "Codes-barres"
    description: "Scan pour validation et réduction des erreurs"
  - title: "Export PDF/CSV"
    description: "Imprimez ou exportez vos listes de picking"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Puis-je définir les emplacements de mes produits ?"
    answer: "Oui, un champ emplacement est ajouté à chaque produit pour optimiser le tri."
  - question: "Le module gère-t-il les déclinaisons ?"
    answer: "Oui, chaque déclinaison peut avoir son propre emplacement."
  - question: "Peut-on utiliser une douchette pour scanner ?"
    answer: "Oui, le module supporte la validation par scan de codes-barres."

testimonial:
  quote: "On prépare 150 commandes/jour au lieu de 80. Le ROI a été immédiat."
  author: "François L."
  role: "Responsable logistique"
  company: "MegaStock.fr"

cta_final:
  title: "Optimisez votre préparation"
  subtitle: "Chaque minute compte. Préparez plus vite, expédiez plus vite."
  button: "Acheter Picking List Pro"

seo:
  meta_title: "Liste de Picking PrestaShop | Préparation Commandes | WePresta"
  meta_description: "Module picking list pour PrestaShop. Optimisez la préparation de commandes, tri par emplacement, validation scan."
  keywords: ["picking", "prestashop", "préparation commandes", "entrepôt", "logistique"]

category: "gestion"
order: 2
```

---

## faq-accordion-pro

```yaml
slug: "faq-accordion-pro"
badge: null
badge_date: null

title: "FAQ Accordion Pro"
tagline: "Répondez aux questions avant qu'on vous les pose"
description: "Créez des FAQ élégantes pour réduire les contacts support et améliorer le SEO. Accordéons, recherche, catégories, et FAQ spécifiques par produit."

stats:
  - value: "-40%"
    label: "Contacts support"
  - value: "SEO"
    label: "Rich Snippets FAQ"
  - value: "Search"
    label: "Recherche intégrée"

price:
  amount: 49
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "FAQ globales et par produit"
    description: "Une FAQ générale + des FAQ spécifiques sur chaque fiche"
  - title: "Accordéons élégants"
    description: "Animation fluide, design personnalisable"
  - title: "Rich Snippets FAQ"
    description: "Questions/réponses affichées dans Google"
  - title: "Recherche instantanée"
    description: "Vos clients trouvent leur réponse en 1 seconde"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Puis-je avoir des FAQ différentes par catégorie ?"
    answer: "Oui, vous pouvez créer des FAQ spécifiques par catégorie, produit ou page CMS."
  - question: "Les FAQ sont-elles indexées par Google ?"
    answer: "Oui, le module génère les balises Schema FAQPage pour l'affichage dans les résultats de recherche."
  - question: "Peut-on importer des FAQ existantes ?"
    answer: "Oui, via un fichier CSV."

testimonial:
  quote: "Nos tickets support ont chuté de 35%. Les clients trouvent leurs réponses seuls."
  author: "Alexandra B."
  role: "Support Manager"
  company: "TechShop.fr"

cta_final:
  title: "Anticipez les questions"
  subtitle: "Une bonne FAQ = moins de support et plus de conversions."
  button: "Acheter FAQ Accordion Pro"

seo:
  meta_title: "Module FAQ PrestaShop | Accordéon & Rich Snippets | WePresta"
  meta_description: "Module FAQ pour PrestaShop avec accordéons, recherche, et rich snippets Google. Réduisez le support, améliorez le SEO."
  keywords: ["faq", "prestashop", "accordion", "rich snippets", "support"]

category: "seo"
order: 3
```

---

## contact-form-builder

```yaml
slug: "contact-form-builder"
badge: null
badge_date: null

title: "Contact Form Builder"
tagline: "Des formulaires qui collectent les bonnes infos"
description: "Créez des formulaires de contact avancés avec drag & drop. Champs conditionnels, pièces jointes, anti-spam, et routage vers le bon service."

stats:
  - value: "Drag"
    label: "& Drop"
  - value: "Anti"
    label: "Spam intégré"
  - value: "RGPD"
    label: "Conforme"

price:
  amount: 59
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Éditeur drag & drop"
    description: "Créez vos formulaires sans coder"
  - title: "Champs conditionnels"
    description: "Affichez des champs selon les réponses précédentes"
  - title: "Pièces jointes"
    description: "Vos clients peuvent joindre des fichiers"
  - title: "Routage intelligent"
    description: "Les messages arrivent au bon service automatiquement"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Puis-je créer plusieurs formulaires ?"
    answer: "Oui, créez autant de formulaires que nécessaire : contact, SAV, demande de devis, etc."
  - question: "Les pièces jointes sont-elles sécurisées ?"
    answer: "Oui, seuls les formats autorisés sont acceptés et les fichiers sont scannés."
  - question: "Le formulaire est-il protégé contre le spam ?"
    answer: "Oui, avec reCAPTCHA v3 invisible ou honeypot intégré."

testimonial:
  quote: "On a réduit les emails mal routés de 80%. Chaque demande arrive au bon service."
  author: "Jean-Marc R."
  role: "Responsable SAV"
  company: "ServicePro.fr"

cta_final:
  title: "Des formulaires qui travaillent"
  subtitle: "Collectez les bonnes informations dès le premier contact."
  button: "Acheter Contact Form Builder"

seo:
  meta_title: "Formulaire Contact PrestaShop | Drag & Drop | WePresta"
  meta_description: "Module formulaire de contact avancé pour PrestaShop. Drag & drop, champs conditionnels, pièces jointes, anti-spam."
  keywords: ["formulaire", "contact", "prestashop", "drag drop", "form builder"]

category: "gestion"
order: 3
```

---

## blog-premium

```yaml
slug: "blog-premium"
badge: null
badge_date: null

title: "Blog Premium"
tagline: "Le contenu qui attire et fidélise"
description: "Un blog complet et SEO-friendly intégré à PrestaShop. Créez du contenu qui génère du trafic et établit votre expertise."

stats:
  - value: "SEO"
    label: "Optimisé"
  - value: "∞"
    label: "Articles"
  - value: "Social"
    label: "Partage intégré"

price:
  amount: 99
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Éditeur riche"
    description: "WYSIWYG complet avec médias, tableaux, citations"
  - title: "SEO avancé"
    description: "Meta personnalisés, URLs propres, sitemap dédié"
  - title: "Produits liés"
    description: "Associez vos articles à vos produits pour les mettre en avant"
  - title: "Commentaires modérés"
    description: "Engagez votre communauté avec les commentaires"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le blog a-t-il son propre sitemap ?"
    answer: "Oui, un sitemap XML dédié est généré pour les articles de blog."
  - question: "Puis-je programmer la publication ?"
    answer: "Oui, planifiez vos articles à l'avance avec la publication différée."
  - question: "Les commentaires sont-ils modérés ?"
    answer: "Oui, vous pouvez approuver chaque commentaire avant publication."

testimonial:
  quote: "Notre blog génère 30% de notre trafic organique. Un investissement rentabilisé en 3 mois."
  author: "Caroline D."
  role: "Content Manager"
  company: "NatureShop.fr"

cta_final:
  title: "Le contenu qui vend"
  subtitle: "Un bon blog attire, éduque et convertit vos visiteurs."
  button: "Acheter Blog Premium"

seo:
  meta_title: "Module Blog PrestaShop | SEO & Contenu | WePresta"
  meta_description: "Module blog SEO-friendly pour PrestaShop. Éditeur riche, produits liés, commentaires modérés."
  keywords: ["blog", "prestashop", "contenu", "seo", "articles"]

category: "seo"
order: 4
```

---

## bulk-product-editor

```yaml
slug: "bulk-product-editor"
badge: "GAIN DE TEMPS"
badge_date: null

title: "Bulk Product Editor"
tagline: "Modifiez 1000 produits en 5 minutes"
description: "Éditeur de masse pour prix, stocks, descriptions, catégories. Interface type tableur pour des modifications ultra-rapides sur tout votre catalogue."

stats:
  - value: "x100"
    label: "Plus rapide"
  - value: "Excel"
    label: "Import/Export"
  - value: "Undo"
    label: "Annulation"

price:
  amount: 119
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Interface tableur"
    description: "Modifiez vos produits comme dans Excel"
  - title: "Actions en masse"
    description: "+10% sur tous les prix, -20% sur une catégorie"
  - title: "Import/Export CSV"
    description: "Exportez, modifiez dans Excel, réimportez"
  - title: "Historique & Undo"
    description: "Annulez vos modifications en un clic"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Quels champs puis-je modifier en masse ?"
    answer: "Prix, quantité, référence, poids, descriptions, meta, catégories, marques, et plus de 50 champs."
  - question: "Puis-je modifier les déclinaisons ?"
    answer: "Oui, chaque déclinaison est éditable individuellement ou en groupe."
  - question: "Le module fait-il une sauvegarde avant modification ?"
    answer: "Oui, une sauvegarde automatique est créée avant chaque modification de masse."

testimonial:
  quote: "Les mises à jour de prix qui prenaient une journée se font maintenant en 10 minutes."
  author: "Stéphane M."
  role: "Category Manager"
  company: "ProShop.fr"

cta_final:
  title: "Gérez votre catalogue efficacement"
  subtitle: "Votre temps est précieux. Arrêtez de cliquer, commencez à éditer."
  button: "Acheter Bulk Product Editor"

seo:
  meta_title: "Édition Produits en Masse PrestaShop | Bulk Editor | WePresta"
  meta_description: "Module d'édition de produits en masse pour PrestaShop. Interface tableur, import/export CSV, historique."
  keywords: ["bulk", "mass edit", "prestashop", "produits", "édition masse"]

category: "gestion"
order: 4
```

---

## advanced-stock-manager

```yaml
slug: "advanced-stock-manager"
badge: null
badge_date: null

title: "Advanced Stock Manager"
tagline: "Zéro rupture, stock optimal"
description: "Gestion de stock avancée avec alertes, prévisions et multi-entrepôts. Anticipez les ruptures et optimisez votre rotation de stock."

stats:
  - value: "0"
    label: "Ruptures"
  - value: "Multi"
    label: "Entrepôts"
  - value: "Auto"
    label: "Alertes"

price:
  amount: 149
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Alertes intelligentes"
    description: "Notification quand un produit approche du seuil minimum"
  - title: "Multi-entrepôts"
    description: "Gérez le stock de plusieurs emplacements"
  - title: "Prévisions de rupture"
    description: "Anticipez les ruptures avec l'analyse des ventes"
  - title: "Mouvements de stock"
    description: "Historique complet de chaque entrée/sortie"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Le module gère-t-il le stock des déclinaisons ?"
    answer: "Oui, chaque déclinaison a son propre stock et ses propres alertes."
  - question: "Puis-je recevoir les alertes par email ?"
    answer: "Oui, alertes par email et/ou notification dans le back-office."
  - question: "Le module se synchronise-t-il avec les marketplaces ?"
    answer: "Le module gère le stock PrestaShop. Pour les marketplaces, utilisez nos connecteurs Amazon/CDiscount."

testimonial:
  quote: "On n'a plus eu une seule rupture depuis 6 mois. Les alertes nous laissent le temps de commander."
  author: "Guillaume T."
  role: "Acheteur"
  company: "StockMax.fr"

cta_final:
  title: "Maîtrisez votre stock"
  subtitle: "Une rupture = une vente perdue. Anticipez, optimisez."
  button: "Acheter Stock Manager"

seo:
  meta_title: "Gestion Stock PrestaShop | Multi-Entrepôts | WePresta"
  meta_description: "Module de gestion de stock avancée pour PrestaShop. Alertes, multi-entrepôts, prévisions de rupture."
  keywords: ["stock", "prestashop", "gestion", "entrepôt", "inventaire"]

category: "gestion"
order: 5
```

---

## wishlist-pro

```yaml
slug: "wishlist-pro"
badge: null
badge_date: null

title: "Wishlist Pro"
tagline: "Transformez les envies en achats"
description: "Listes d'envies complètes avec partage social, alertes prix et relances automatiques. Convertissez les visiteurs qui hésitent."

stats:
  - value: "+20%"
    label: "Retours visiteurs"
  - value: "Share"
    label: "Partage social"
  - value: "Alert"
    label: "Baisse de prix"

price:
  amount: 79
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Listes multiples"
    description: "Vos clients créent plusieurs wishlists thématiques"
  - title: "Partage social"
    description: "Partagez par email, Facebook, WhatsApp pour les cadeaux"
  - title: "Alerte baisse de prix"
    description: "Notification automatique quand un produit baisse"
  - title: "Relance abandon"
    description: "Email automatique : Vos produits sont encore là"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "La wishlist fonctionne-t-elle sans compte ?"
    answer: "Oui, les visiteurs peuvent ajouter des produits, puis créer un compte pour sauvegarder."
  - question: "Les alertes sont-elles personnalisables ?"
    answer: "Oui, vous définissez le % de baisse qui déclenche l'alerte."
  - question: "Puis-je voir les wishlists de mes clients ?"
    answer: "Oui, vous avez accès aux statistiques : produits les plus ajoutés, taux de conversion wishlist→achat."

testimonial:
  quote: "Les alertes de baisse de prix convertissent à 15%. Un canal de vente sous-estimé."
  author: "Émilie F."
  role: "Digital Marketing"
  company: "FashionStore.fr"

cta_final:
  title: "L'envie devient achat"
  subtitle: "Chaque produit en wishlist est une opportunité de vente."
  button: "Acheter Wishlist Pro"

seo:
  meta_title: "Module Wishlist PrestaShop | Liste d'Envies | WePresta"
  meta_description: "Module wishlist pour PrestaShop. Listes multiples, partage social, alertes prix, relances automatiques."
  keywords: ["wishlist", "prestashop", "liste envies", "favoris"]

category: "ventes"
order: 1
```

---

## gift-card-system

```yaml
slug: "gift-card-system"
badge: null
badge_date: null

title: "Gift Card System"
tagline: "Les cartes cadeaux qui boostent votre CA"
description: "Vendez des cartes cadeaux personnalisables avec designs premium, envoi programmé et gestion complète. Le cadeau parfait pour vos clients."

stats:
  - value: "+15%"
    label: "CA additionnel"
  - value: "20+"
    label: "Designs inclus"
  - value: "Auto"
    label: "Envoi programmé"

price:
  amount: 129
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Montants flexibles"
    description: "Montants prédéfinis ou personnalisés par le client"
  - title: "Designs premium"
    description: "20+ templates pour toutes les occasions"
  - title: "Message personnalisé"
    description: "Le client ajoute un message au destinataire"
  - title: "Envoi programmé"
    description: "Planifiez l'envoi pour un anniversaire"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les cartes ont-elles une date d'expiration ?"
    answer: "Vous choisissez : sans limite ou avec durée de validité configurable."
  - question: "Puis-je utiliser partiellement une carte cadeau ?"
    answer: "Oui, le solde restant est conservé pour les prochains achats."
  - question: "Les cartes sont-elles cumulables avec les promos ?"
    answer: "Vous définissez les règles : cumul autorisé ou non avec les promotions."

testimonial:
  quote: "Les cartes cadeaux représentent 12% de notre CA à Noël. Un must-have."
  author: "Patrick L."
  role: "Directeur commercial"
  company: "CadeauxShop.fr"

cta_final:
  title: "Vendez du bonheur"
  subtitle: "Les cartes cadeaux : revenus garantis, clients nouveaux."
  button: "Acheter Gift Card System"

seo:
  meta_title: "Cartes Cadeaux PrestaShop | Gift Card | WePresta"
  meta_description: "Module cartes cadeaux pour PrestaShop. Designs premium, envoi programmé, gestion complète du solde."
  keywords: ["carte cadeau", "gift card", "prestashop", "bon achat"]

category: "ventes"
order: 2
```

---

## points-rewards

```yaml
slug: "points-rewards"
badge: null
badge_date: null

title: "Points & Rewards"
tagline: "La fidélité qui fait revenir"
description: "Programme de fidélité complet avec points, niveaux et récompenses. Transformez vos clients ponctuels en ambassadeurs de votre marque."

stats:
  - value: "+35%"
    label: "Rétention"
  - value: "5"
    label: "Niveaux VIP"
  - value: "Auto"
    label: "Attribution"

price:
  amount: 149
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Points sur achats"
    description: "1€ = X points, configurable par catégorie"
  - title: "Niveaux VIP"
    description: "Bronze, Silver, Gold, Platinum avec avantages croissants"
  - title: "Récompenses variées"
    description: "Bons de réduction, livraison gratuite, produits offerts"
  - title: "Parrainage"
    description: "Points pour le parrain et le filleul"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les points expirent-ils ?"
    answer: "Vous choisissez : sans expiration ou avec durée de validité."
  - question: "Puis-je donner des points bonus ?"
    answer: "Oui, ajoutez des points manuellement ou via des actions bonus (avis, anniversaire, inscription)."
  - question: "Le programme est-il visible sur le compte client ?"
    answer: "Oui, avec historique des points, niveau actuel et récompenses disponibles."

testimonial:
  quote: "Notre taux de réachat est passé de 18% à 42% en 6 mois. Le programme fidélité change tout."
  author: "Isabelle P."
  role: "Directrice marketing"
  company: "BioMarket.fr"

cta_final:
  title: "Fidélisez pour toujours"
  subtitle: "Un client fidèle coûte 5x moins cher qu'un nouveau."
  button: "Acheter Points & Rewards"

seo:
  meta_title: "Programme Fidélité PrestaShop | Points & Rewards | WePresta"
  meta_description: "Module programme de fidélité pour PrestaShop. Points, niveaux VIP, parrainage, récompenses automatiques."
  keywords: ["fidélité", "points", "rewards", "prestashop", "loyalty"]

category: "ventes"
order: 3
```

---

## cross-sell-bundles

```yaml
slug: "cross-sell-bundles"
badge: null
badge_date: null

title: "Cross-Sell & Product Bundles"
tagline: "Le panier qui grossit tout seul"
description: "Augmentez le panier moyen avec des suggestions intelligentes et des packs produits attractifs. Les clients qui ont acheté X ont aussi acheté Y."

stats:
  - value: "+25%"
    label: "Panier moyen"
  - value: "IA"
    label: "Suggestions auto"
  - value: "Bundle"
    label: "Packs attractifs"

price:
  amount: 119
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Suggestions automatiques"
    description: "Produits associés basés sur l'historique d'achats"
  - title: "Bundles avec réduction"
    description: "Créez des packs avec prix attractif"
  - title: "Frequently Bought Together"
    description: "Les clients achètent souvent ensemble..."
  - title: "Upsell panier"
    description: "Suggestions avant validation du panier"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les suggestions sont-elles automatiques ?"
    answer: "Oui, le module analyse les commandes passées. Vous pouvez aussi définir des associations manuelles."
  - question: "Le stock du bundle est-il géré automatiquement ?"
    answer: "Oui, le stock est basé sur le produit du bundle avec le moins de stock."
  - question: "Puis-je avoir plusieurs bundles par produit ?"
    answer: "Oui, créez autant de bundles que vous voulez."

testimonial:
  quote: "Notre panier moyen est passé de 65€ à 89€. Les bundles se vendent comme des petits pains."
  author: "Mathieu C."
  role: "E-commerce Manager"
  company: "SportWorld.fr"

cta_final:
  title: "Vendez plus à chaque visite"
  subtitle: "Chaque client peut acheter plus. Montrez-lui quoi."
  button: "Acheter Cross-Sell & Bundles"

seo:
  meta_title: "Cross-Sell Bundles PrestaShop | Panier Moyen | WePresta"
  meta_description: "Module cross-sell et bundles pour PrestaShop. Suggestions automatiques, packs produits, augmentez le panier moyen."
  keywords: ["cross-sell", "bundles", "prestashop", "panier moyen", "upsell"]

category: "ventes"
order: 4
```

---

## ultimate-banners-sliders

```yaml
slug: "ultimate-banners-sliders"
badge: null
badge_date: null

title: "Ultimate Banners & Sliders"
tagline: "Des visuels qui captivent et convertissent"
description: "Créez des bannières et sliders spectaculaires sans coder. Animations, responsive, A/B testing et intégration parfaite avec votre thème."

stats:
  - value: "50+"
    label: "Animations"
  - value: "Drag"
    label: "& Drop"
  - value: "A/B"
    label: "Testing"

price:
  amount: 89
  currency: "€"
  billing: "HT · TVA applicable"

license_options:
  sites: ["1 site", "5 sites", "25 sites", "100 sites"]
  duration: ["1 an", "À vie"]

includes:
  - "Licence pour le nombre de sites choisi"
  - "Mises à jour selon durée choisie"
  - "Support par email"
  - "Documentation complète"

features:
  - title: "Éditeur visuel"
    description: "Créez vos bannières en drag & drop"
  - title: "50+ animations"
    description: "Effets d'entrée, survol, transitions spectaculaires"
  - title: "100% responsive"
    description: "Parfait sur mobile, tablette et desktop"
  - title: "Programmation"
    description: "Planifiez vos bannières promo à l'avance"

compatibility:
  prestashop: ["8.1", "8.2", "9.0"]
  php: ["8.1", "8.2", "8.3"]
  themes: ["Hummingbird", "Classic", "Tous thèmes"]

faq:
  - question: "Les sliders ralentissent-ils le site ?"
    answer: "Non, le module utilise le lazy loading et les images sont optimisées automatiquement."
  - question: "Puis-je afficher des bannières différentes par catégorie ?"
    answer: "Oui, vous définissez où afficher chaque bannière : accueil, catégorie, produit, etc."
  - question: "Le module supporte-t-il les vidéos ?"
    answer: "Oui, intégrez des vidéos YouTube ou des fichiers MP4."

testimonial:
  quote: "On change nos bannières toutes les semaines sans toucher au code. Le module est super intuitif."
  author: "Laura K."
  role: "Webdesigner"
  company: "DesignShop.fr"

cta_final:
  title: "Des visuels qui vendent"
  subtitle: "Une belle bannière = plus de clics. Créez la vôtre."
  button: "Acheter Ultimate Banners"

seo:
  meta_title: "Bannières Sliders PrestaShop | Module | WePresta"
  meta_description: "Module bannières et sliders pour PrestaShop. Éditeur drag & drop, 50+ animations, responsive, A/B testing."
  keywords: ["bannières", "sliders", "prestashop", "carousel", "animations"]

category: "marketing"
order: 6
```

---

# Packs

## pack-starter

```yaml
slug: "pack-starter"
title: "Pack Starter"
tagline: "Tout pour démarrer sereinement"
description: "Les modules essentiels pour une boutique conforme et efficace."

modules_included:
  - "rgpd-cookie-consent-pro"
  - "mentions-legales-generator"
  - "smart-popup-exit-intent"
  - "faq-accordion-pro"
  - "contact-form-builder"
  - "newsletter-subscription"

price:
  regular: 384
  pack: 299
  discount: "-22%"

cta: "Acheter le Pack Starter"
```

---

## pack-seo-marketing

```yaml
slug: "pack-seo-marketing"
title: "Pack SEO & Marketing"
tagline: "Boostez votre visibilité et vos conversions"
description: "Les meilleurs outils pour attirer du trafic et convertir vos visiteurs."

modules_included:
  - "seo-manager-360"
  - "rich-snippets-schema"
  - "cart-recovery-email"
  - "product-reviews-ratings"
  - "social-proof-notifications"
  - "ultimate-banners-sliders"

price:
  regular: 664
  pack: 499
  discount: "-25%"

cta: "Acheter le Pack SEO & Marketing"
```

---

## pack-business

```yaml
slug: "pack-business"
title: "Pack Business"
tagline: "Pour les e-commerces ambitieux"
description: "Tous les modules Starter + SEO & Marketing pour une boutique performante."

modules_included:
  - "Tous les modules Pack Starter"
  - "Tous les modules Pack SEO & Marketing"

price:
  regular: 1048
  pack: 699
  discount: "-33%"

cta: "Acheter le Pack Business"
```

---

## pack-enterprise

```yaml
slug: "pack-enterprise"
title: "Pack Enterprise"
tagline: "La solution complète pour dominer"
description: "Tous les modules WePresta pour une boutique e-commerce optimale."

modules_included:
  - "Tous les 24 modules du catalogue"

price:
  regular: 2574
  pack: 1499
  discount: "-42%"

cta: "Acheter le Pack Enterprise"
```

---

# Pages statiques

## homepage

```yaml
hero:
  title: "Modules PrestaShop Premium"
  subtitle: "Qualité suisse, code propre, support expert"
  cta_primary: "Découvrir les modules"
  cta_secondary: "Voir les packs"

stats:
  - value: "24+"
    label: "Modules"
  - value: "500+"
    label: "Boutiques équipées"
  - value: "4.9/5"
    label: "Note moyenne"

featured_modules:
  - "rgpd-cookie-consent-pro"
  - "seo-manager-360"
  - "cart-recovery-email"
  - "google-shopping-feed"

testimonials:
  - quote: "Enfin des modules qui fonctionnent du premier coup."
    author: "Marie L."
    company: "BoutiqueMode.fr"
  - quote: "Support réactif et documentation complète."
    author: "Thomas R."
    company: "SportShop.fr"
```

---

## about

```yaml
title: "À propos de WePresta"
content: |
  WePresta développe des modules PrestaShop premium depuis la Suisse.
  
  Notre philosophie :
  - Code propre et documenté
  - Support rapide et expert
  - Mises à jour régulières
  - Conformité légale garantie

team:
  - name: "Bruno Studer"
    role: "Fondateur & Lead Developer"
    bio: "15 ans d'expérience e-commerce, expert PrestaShop certifié."
```

---

*Fin du plan de contenu*

