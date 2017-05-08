<?php
require_once __DIR__.'/../vendor/autoload.php';
use Funda\FundaAnalytics;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app = new Silex\Application();

$app['debug'] = true;

$hostname = $_SERVER['DB_HOSTNAME'];
$username = $_SERVER['DB_USERNAME'];
$password = $_SERVER['DB_PASSWORD'];
$dbname = $_SERVER['DB_NAME'];

$app->register(new Silex\Provider\DoctrineServiceProvider(), [
    'db.options' => [
        'driver'    => 'pdo_mysql',
        'host'      => $hostname,
        'dbname'    => $dbname,
        'user'      => $username,
        'password'  => $password,
        'charset'   => 'utf8mb4'
    ],
]);

$app->before(function (Request $request) {
    if (0 === strpos($request->headers->get('Content-Type'), 'application/json')) {
        $data = json_decode($request->getContent(), true);
        $request->request->replace(is_array($data) ? $data : []);
    }
});

$app->get('/funda/topmakelaars',  'Funda\Controllers\Funda::topMakelaars');

$app->get('/funda/topzipcodes',  'Funda\Controllers\Funda::topZipcodes');

$app->after(function (Request $request, Response $response) {
    $response->headers->set('Content-Type', 'application/json');
});

$app->run();