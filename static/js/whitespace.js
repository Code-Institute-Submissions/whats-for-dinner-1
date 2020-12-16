// Credit to http://www.nullskull.com/q/10393870/white-space-validation-in-javascript.aspx for code below

function isSpacesOnly(field) {
  const r = field.value.replace(/\s/g, '');
  return (r.length === 0);
}
