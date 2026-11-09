// BEconomics: menu toggle and contact form
document.documentElement.classList.add('js');

(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'סגירה' : 'תפריט';
    });
  }

  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = form.querySelector('.form-status');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form._honey && form._honey.value) return;
    var data = new FormData(form);
    var button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    status.className = 'form-status';
    status.textContent = 'שולח…';
    fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function () {
        form.reset();
        status.className = 'form-status ok';
        status.textContent = 'ההודעה נשלחה. נחזור אליך בהקדם.';
      })
      .catch(function () {
        status.className = 'form-status err';
        status.innerHTML = 'ההודעה לא נשלחה. אפשר לכתוב ישירות ל-<a href="mailto:tiran@b-economics.com">tiran@b-economics.com</a> או בוואטסאפ.';
      })
      .finally(function () { button.disabled = false; });
  });
})();
