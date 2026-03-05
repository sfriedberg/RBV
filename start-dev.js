process.chdir(__dirname);
process.argv.push('dev', '--port', '3001');
require('./node_modules/next/dist/bin/next');
