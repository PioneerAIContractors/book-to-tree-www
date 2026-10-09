// Fills the "See an example" excerpts from the files in sample/, so replacing those files
// updates the page. The page shown is set by data-page on #example (the CSV's image number).
(function () {
  var section = document.getElementById("example");
  if (!section) return;
  var page = section.getAttribute("data-page");

  // Minimal CSV parser: quoted fields, doubled quotes, commas and newlines inside quotes.
  function parseCSV(text) {
    var rows = [], row = [], field = "", inQuotes = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQuotes) {
        if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
        else if (c === '"') inQuotes = false;
        else field += c;
      } else if (c === '"') inQuotes = true;
      else if (c === ",") { row.push(field); field = ""; }
      else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
      else if (c !== "\r") field += c;
    }
    if (field !== "" || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  // If a file can't be read, hide its whole card rather than show an empty box.
  function hide(el) {
    var box = el && (el.closest(".ex-card") || el);
    if (box) box.style.display = "none";
  }

  var table = document.getElementById("sample-rows");
  // Column names, repeated on each cell so phones can show one block per person.
  var labels = Array.prototype.map.call(table.querySelectorAll("thead th"), function (th) {
    return th.textContent;
  });
  fetch("sample/extracted.csv")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then(function (text) {
      var rows = parseCSV(text), head = rows[0];
      var col = function (name) { return head.indexOf(name); };
      var img = col("image"), name = col("name"), bd = col("birth_date"),
          bp = col("birth_place"), dd = col("death_date");
      var body = table.querySelector("tbody"), shown = 0;
      for (var i = 1; i < rows.length && shown < 6; i++) {
        var r = rows[i];
        if (r[img] !== page || !(r[bd] || r[dd])) continue;
        var tr = document.createElement("tr");
        tr.setAttribute("role", "row");
        [r[name], r[bd], r[bp], r[dd]].forEach(function (v, k) {
          var td = document.createElement("td");
          td.setAttribute("role", "cell");
          td.setAttribute("data-label", labels[k] || "");
          td.textContent = v || "";
          tr.appendChild(td);
        });
        // Phones show the name plus these short lines instead of the three columns.
        var born = r[bd] ? "b. " + r[bd] + (r[bp] ? ", " + r[bp] : "") : (r[bp] || "");
        var sum = document.createElement("td");
        sum.className = "sum";
        sum.setAttribute("role", "cell");
        [born, r[dd] ? "d. " + r[dd] : ""].filter(Boolean).forEach(function (t) {
          var s = document.createElement("span");
          s.textContent = t;
          sum.appendChild(s);
        });
        tr.appendChild(sum);
        body.appendChild(tr); shown++;
      }
      if (!shown) hide(table);
    })
    .catch(function () { hide(table); });

  var pre = document.getElementById("sample-gedcom");
  fetch("sample/tree.ged")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then(function (text) {
      // The first person record that cites the page shown.
      var records = text.replace(/\r/g, "").split(/\n(?=0 )/);
      var cite = new RegExp("^2 PAGE " + page + "$", "m");
      var onPage = records.filter(function (block) {
        return / INDI$/m.test(block.split("\n")[0]) && cite.test(block);
      });
      // PREFER A RECORD THAT SHOWS THE FORMAT. Many people on a page are named only as
      // somebody's spouse, with no dates of their own; the first record citing the page is
      // as likely to be one of those as not, and it demonstrates nothing. Take the first
      // that carries a birth or a death, and fall back to the first if none do.
      // A record with an actual DATE, not merely a BIRT with a place under it — the panel
      // exists to show what a filled-in person looks like.
      var rec = onPage.filter(function (b) { return /^2 DATE /m.test(b); })[0] || onPage[0];
      if (!rec) { hide(pre); return; }
      // Mark the source citation (SOUR and its PAGE), the lines that tie a person to a page.
      // Phones show only the record's header, name, birth, death and citation; each run of
      // other lines collapses to a "⋮" there (.ged-more and .ged-gap in site.css).
      var KEEP1 = { NAME: 1, BIRT: 1, DEAT: 1, SOUR: 1 }, KEEP2 = { BIRT: 1, DEAT: 1, SOUR: 1 };
      var parent = "", prevKept = true;
      rec.trim().split("\n").forEach(function (line, i, all) {
        var m = /^(\d+) (\S+)/.exec(line) || [];
        if (m[1] === "1") parent = m[2];
        var kept = i === 0 || (m[1] === "1" && KEEP1[m[2]]) || (m[1] === "2" && KEEP2[parent]);
        if (!kept && prevKept) {
          var gap = document.createElement("span");
          gap.className = "ged-gap";
          gap.setAttribute("aria-hidden", "true");
          gap.textContent = "⋮\n";
          pre.appendChild(gap);
        }
        prevKept = kept;
        var cite = /^1 SOUR /.test(line) || (/^2 PAGE /.test(line) && /^1 SOUR /.test(all[i - 1] || ""));
        var wrap = document.createElement("span");
        if (!kept) wrap.className = "ged-more";
        var text = document.createTextNode(line);
        if (cite) { var mk = document.createElement("mark"); mk.appendChild(text); text = mk; }
        wrap.appendChild(text);
        if (i < all.length - 1) wrap.appendChild(document.createTextNode("\n"));
        pre.appendChild(wrap);
      });
    })
    .catch(function () { hide(pre); });
})();
