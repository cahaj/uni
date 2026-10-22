#!/usr/bin/env node
/* Build the browser files of highlight.js that the file viewer loads on demand.

   Usage:
     npm install highlight.js esbuild          (anywhere, e.g. a temp folder)
     node build_hljs.cjs <node_modules/highlight.js> <out dir> [language ...]

   With no language arguments the default list below is built. Output:
     <out>/hljs.js         core, defines window.hljs
     <out>/langs/<id>.js   one file per language, registers itself on window.hljs
     <out>/LICENSE, VERSION

   The viewer's output lives in .github/site/viewer/vendor/. A new language only
   needs its file in langs/; viewer.py then picks it up (add the file extension
   to its LANGUAGES table so files are mapped to it).

   Tested with highlight.js 10.7.3. */
const fs = require('fs');
const path = require('path');
const esbuild = require('esbuild');

const DEFAULT_LANGS = (
  'abnf ada apache arduino armasm avrasm awk bash basic bnf c clojure cmake coffeescript coq cpp ' +
  'crystal csharp css d dart delphi diff django dockerfile dos ebnf elixir elm erb erlang fortran ' +
  'fsharp gcode gherkin glsl go gradle groovy handlebars haskell haxe http ini java javascript json ' +
  'julia kotlin latex less lisp llvm lua makefile matlab mipsasm nginx nim nix objectivec ocaml ' +
  'openscad perl pgsql php powershell prolog properties protobuf python r ruby rust scala scheme ' +
  'scss shell smalltalk sml sql stylus swift tcl thrift twig typescript vbnet vbscript verilog vhdl ' +
  'vim x86asm xml yaml'
).split(/\s+/);

const [pkg, out, ...langs] = process.argv.slice(2);
if (!pkg || !out) {
  console.error('usage: node build_hljs.cjs <highlight.js package dir> <out dir> [language ...]');
  process.exit(1);
}
const list = langs.length ? langs : DEFAULT_LANGS;
const lib = path.resolve(pkg, 'lib');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(path.join(out, 'langs'), { recursive: true });

const common = { bundle: true, minify: true, format: 'iife', legalComments: 'none', logLevel: 'warning' };

esbuild.buildSync({ ...common, entryPoints: [path.join(lib, 'core.js')],
  globalName: 'hljs', outfile: path.join(out, 'hljs.js') });

for (const name of list) {
  const file = path.join(lib, 'languages', name + '.js');
  if (!fs.existsSync(file)) { console.error('no such language: ' + name); process.exit(1); }
  esbuild.buildSync({ ...common,
    stdin: { contents: `hljs.registerLanguage(${JSON.stringify(name)}, require(${JSON.stringify(file)}));`,
             resolveDir: lib },
    outfile: path.join(out, 'langs', name + '.js') });
}

fs.copyFileSync(path.join(pkg, 'LICENSE'), path.join(out, 'LICENSE'));
const version = JSON.parse(fs.readFileSync(path.join(pkg, 'package.json'), 'utf8')).version;
fs.writeFileSync(path.join(out, 'VERSION'), `highlight.js ${version}\n`);
console.log(`built highlight.js ${version}: core + ${list.length} languages -> ${out}`);
