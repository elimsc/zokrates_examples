// 16进制转10进制 num为16进制 字符串
function hexToBig(num) {
  return BigInt(num)
}

// 10进制转16进制, num为10进制 数
function bigToHex(num) {
  return '0x' + BigInt(num).toString(16)
}

// string => Uint8Array
function strToU8arr(str) {
  return new TextEncoder('utf-8').encode(str)
}

// Uint8Array => string
function u8arrToStr(u8arr) {
  return new TextDecoder('utf-8').decode(u8arr)
}

// bigint => Uint8Array
function bigToU8arr(big) {
  const big0 = BigInt(0)
  const big1 = BigInt(1)
  const big8 = BigInt(8)
  if (big < big0) {
    const bits = (BigInt(big.toString(2).length) / big8 + big1) * big8
    const prefix1 = big1 << bits
    big += prefix1
  }
  let hex = big.toString(16)
  if (hex.length % 2) {
    hex = '0' + hex
  }
  const len = hex.length / 2
  const u8 = new Uint8Array(len)
  var i = 0
  var j = 0
  while (i < len) {
    u8[i] = parseInt(hex.slice(j, j + 2), 16)
    i += 1
    j += 2
  }
  return u8
}

// Uint8Array => bigint
function u8arrToBig(buf) {
  var hex = [];
  u8 = Uint8Array.from(buf);

  u8.forEach(function (i) {
    var h = i.toString(16);
    if (h.length % 2) { h = '0' + h; }
    hex.push(h);
  });

  return BigInt('0x' + hex.join(''));
}

function u32arrToHex(u32Arr) {
  var hex = [];
  u32 = Uint32Array.from(u32Arr)
  u32.forEach(function (i) {
    var h = i.toString(16);
    hex.push('0'.repeat(8 - h.length) + h)
  })
  return '0x' + hex.join('');
}

// string => bigint
function strToBig(str) {
  return u8arrToBig(strToU8arr(str));
}

// bigint => string
function bigToStr(big) {
  return u8arrToStr(bigToU8arr(big));
}

// test
// (function test() {
//   const big = 65392825175610104415632231972613810024n;
//   var str = '12345678abcdefgh';
//   const u8arr = new Uint8Array([49, 50, 51, 52, 53, 54, 55, 56, 97, 98, 99, 100, 101, 102, 103, 104]);
//   console.assert(hexToBig(bigToHex(big)) == big);
//   console.assert(bigToStr(big) == str);
//   console.assert(strToBig(str) == big);
//   console.assert(u8arrToBig(u8arr) == big);

//   const u32arr = new Uint32Array([50, 51, 52, 53, 54, 55, 56, 57]);
//   console.log(u32arrToHex(u32arr) == '0x0000003200000033000000340000003500000036000000370000003800000039')
//   console.log(hexToBig('' + u32arrToHex(u32arr)))

//   // 0x0000003200000033000000340000003500000036000000370000003800000039
//   // 1347997333677664178314069558465848711463127878989839168093184396886073
//   console.log(hexToBig('0x0000003200000033000000340000003500000036000000370000003800000039'));
//   // 36341936214780344529475692710416345157619370405341114642424254771276096654052387990787801629949271340173321900549085200726559466178215993
// })();

hl = bigToHex(125098319466480357781252412499135627896n);
hh = bigToHex(213891364127076091963521468168519447550n);
h = hh + hl.replace("0x", "");
console.log(h)

