(function () {
  var WA = '35799335570';

  // Mobile menu
  var btn = document.querySelector('.menu-toggle');
  var menu = document.getElementById('menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Source tagging: both Volan websites share the same WhatsApp number and
  // email, so every WhatsApp chat and email from this site is pre-filled
  // with "Volan Premium Transfers" to show where the enquiry came from.
  var SITE = 'Volan Premium Transfers';
  var PAGES = {
    '/': 'Home',
    '/larnaca-airport-transfers/': 'Larnaca Airport Transfers',
    '/paphos-airport-transfers/': 'Paphos Airport Transfers',
    '/limassol-transfers/': 'Limassol Transfers',
    '/ayia-napa-protaras-transfers/': 'Ayia Napa & Protaras Transfers',
    '/group-bus-hire-cyprus/': 'Group Bus Hire',
    '/private-tours-cyprus/': 'Private Tours'
  };
  var path = location.pathname.replace(/index\.html$/, '');
  if (path.slice(-1) !== '/') path += '/';
  var pageName = PAGES[path] || '';
  var waText = 'Hello ' + SITE + '! I would like a quote.';
  var mailSubject = 'Quote request - ' + SITE + (pageName ? ' (' + pageName + ')' : '');
  var links = document.querySelectorAll('a[href]');
  for (var i = 0; i < links.length; i++) {
    var href = links[i].getAttribute('href');
    if (/^https:\/\/wa\.me\/\d+\/?$/.test(href)) {
      links[i].setAttribute('href', href.replace(/\/$/, '') + '?text=' + encodeURIComponent(waText));
    } else if (/^mailto:[^?]+$/.test(href)) {
      links[i].setAttribute('href', href + '?subject=' + encodeURIComponent(mailSubject));
    }
  }

  // Analytics helper (GA4)
  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('wa.me') !== -1) track('whatsapp_click', { link_location: a.dataset.loc || 'page' });
    else if (href.indexOf('tel:') === 0) track('phone_click', { link_location: a.dataset.loc || 'page' });
    else if (href.indexOf('mailto:') === 0) track('email_click', { link_location: a.dataset.loc || 'page' });
  });

  // Quote form -> WhatsApp
  var form = document.getElementById('quote-form');
  if (form) {
    var date = form.querySelector('[name=date]');
    if (date) date.min = new Date().toISOString().slice(0, 10);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements;
      var lines = [
        'Hello Volan Premium Transfers! I would like a quote.',
        '',
        'Name: ' + f.name.value,
        'Phone/WhatsApp: ' + f.phone.value,
        'From: ' + f.pickup.value,
        'To: ' + f.dropoff.value,
        'Date: ' + f.date.value + ' ' + f.time.value,
        'Passengers: ' + (f.pax.value || '-'),
        'Flight number: ' + (f.flight.value || '-'),
        'Notes: ' + (f.notes.value || '-')
      ];
      track('generate_lead', { method: 'whatsapp_form', page: location.pathname });
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }
})();
